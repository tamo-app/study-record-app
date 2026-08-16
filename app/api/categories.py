"""
目的:カテゴリ関係のAPIを定義
入力:HTTPリクエスト
出力:HTTPレスポンス
副作用:現在はなし(DB接続後はDB更新)
前提条件:main.pyでAPIrouterの登録
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.auth import get_current_user
from app.dependencies import get_db
from app.models.categories import Category
from app.models.records import Record
from app.schemas.category import CreateCategory, CreateCategoryResponse, GetCategoryResponse, UpdateCategory, UpdateCategoryResponse, DeleteCategoryResponse

router = APIRouter(prefix="/categories")

# カテゴリ一覧を見る
@router.get("/", response_model = GetCategoryResponse)
def get_categories(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Category).where(Category.user_id == user_id)
    result = db.execute(stmt)
    categories = result.scalars().all()

    return {
        "message":"get categories successfully",
        "categories":categories
        }

# カテゴリを作成する
@router.post("/", response_model = CreateCategoryResponse)
def create_category(
    request: CreateCategory,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_category = Category(
        user_id = user_id,
        name = request.name,
        detail = request.detail
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return {
        "message":"create category successfully",
        "id":new_category.id
    }

# カテゴリを編集する
@router.put("/{category_id}", response_model = UpdateCategoryResponse)
def update_category(
    category_id: int,
    request: UpdateCategory,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Category).where(Category.id == category_id, Category.user_id == user_id)
    result = db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
        status_code = 404,
        detail = "Category not found"
    )

    category.name = request.name
    category.detail = request.detail
    db.commit()

    return {
        "message":"update category successfully", 
        "category_id": category_id
    }

# カテゴリを削除する
@router.delete("/{category_id}", response_model = DeleteCategoryResponse)
def delete_category(
    category_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Category).where(Category.id == category_id, Category.user_id == user_id)
    result = db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
        status_code = 404,
        detail = "Category not found"
    )

    # 削除対象のカテゴリを持ってるレコードが残ってたらカテゴリは削除できない
    stmt = select(Record).where(Record.category_id == category_id)
    result = db.execute(stmt)
    record = result.scalar_one_or_none()
    if  record:
        raise HTTPException(
        status_code = 409,
        detail = "Category cannot be deleted because records exist"
    )

    db.delete(category)
    db.commit()

    return {
        "message":"delete category successfully",
        "category_id": category_id
    }