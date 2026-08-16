"""
目的:学習記録関係のAPIを定義
入力:HTTPリクエスト
出力:HTTPレスポンス
副作用:現在はなし(DB接続後はDB更新)
前提条件:main.pyでAPIrouterの登録
"""

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.auth import get_current_user
from app.dependencies import get_db
from app.models.records import Record
from app.models.categories import Category
from app.schemas.record import SummaryResponse, CreateRecord, CreateRecordResponse, GetAllRecordsResponse, GetRecordResponse, UpdateRecord, UpdateRecordResponse, DeleteRecordResponse

router = APIRouter(prefix="/records")

# カテゴリごとの学習時間を集計する
@router.get("/summary/", response_model = SummaryResponse)
def summary_minutes(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = (
        select(
                Category.name,
                func.sum(Record.study_minutes)
        )
            .join(Category, 
                  (Record.category_id == Category.id) 
                  & (Category.user_id == user_id))
            .where(Record.user_id == user_id)
            .group_by(Category.id, Category.name)
            )
    result = db.execute(stmt)
    rows = result.all()

    # 1行を、"category_name": XX,"study_minutes": YYの形にする
    summary =  [
            {
            "category_name": row[0],
            "study_minutes": row[1]
            }
            for row in rows
        ]
    
    return {
        "message": "summary get successfully!",
        "summary": summary
    }

# 学習記録の一覧を見る
@router.get("/", response_model = GetAllRecordsResponse)
def get_all_records(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Record).where(Record.user_id == user_id)
    result = db.execute(stmt)
    records = result.scalars().all()

    # 1件ずつrecordを取り出してid,category_name,title,study_minutesを取得
    record_list = [
        {
            "id": record.id,
            "category_name": record.category.name,
            "title": record.title,
            "study_minutes": record.study_minutes
        }
            for record in records
    ]

    return {
        "message": "all records get successfully!",
        "records": record_list
    }

# 学習記録の詳細を見る
@router.get("/{record_id}", response_model = GetRecordResponse)
def get_record(
    record_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Record).where(Record.id == record_id, Record.user_id == user_id)
    result = db.execute(stmt)
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(
            status_code = 404,
            detail = "Record not found"
        )
    
    return {"message": "record get successfully!",
            "record": {
            "id": record.id,
            "category_name": record.category.name,
            "title": record.title,
            "study_minutes": record.study_minutes,
            "detail": record.detail
        }
    }

# 学習記録を作成する
@router.post("/", response_model = CreateRecordResponse)
def create_record(
    request: CreateRecord,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_record = Record(
        user_id = user_id,
        title = request.title,
        category_id = request.category_id,
        study_minutes = request.study_minutes,
        detail = request.detail
    )
    stmt = select(Category).where(
    Category.id == request.category_id,
    Category.user_id == user_id
)
    result = db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "record created successfully!",
        "id": new_record.id,
        "title": new_record.title
    }

# 学習記録を編集する
@router.put("/{record_id}", response_model = UpdateRecordResponse)
def update_record(
    record_id: int,
    request: UpdateRecord,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ログインユーザーのレコードかチェック
    stmt = select(Record).where(
        Record.id == record_id, 
        Record.user_id == user_id
        )
    result = db.execute(stmt)
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(
            status_code = 404,
            detail = "Record not found"
        )
    # 変更先のカテゴリはログインユーザーのものかチェック
    stmt = select(Category).where(
        Category.id == request.category_id, 
        Category.user_id == user_id
        )
    result = db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
    )

    record.category_id = request.category_id
    record.title= request.title
    record.study_minutes = request.study_minutes
    record.detail = request.detail
    db.commit()

    return {
        "message": "record update successfully!", 
        "title": request.title
    }

# 学習記録を削除する
@router.delete("/{record_id}", response_model = DeleteRecordResponse)
def delete_record(
    record_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    stmt = select(Record).where(Record.id == record_id, Record.user_id == user_id)
    result = db.execute(stmt)
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(
        status_code = 404,
        detail = "Record not found"
    )

    db.delete(record)
    db.commit()
    return {
        "message": "record delete successfully!",
        "record_id": record_id
    }
