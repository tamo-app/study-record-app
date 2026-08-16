"""
目的:ユーザー関係のAPIを定義
入力:HTTPリクエスト
出力:HTTPレスポンス
副作用:現在はなし(DB接続後はDB更新)
前提条件:main.pyでAPIrouterの登録
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dependencies import get_db
from app.models.users import User
from app.schemas.user import UserCreate, UserCreateResponse, UserDetailResponse, UserUpdate, UserUpdateResponse, UserDeleteResponse, LoginResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user
router = APIRouter(prefix="/users")

# ユーザー詳細を見る
@router.get("/", response_model = UserDetailResponse)
def get_user(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
    )
    
    return {
        "message": "user get successfully!",
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

# ユーザー作成
@router.post("/", response_model = UserCreateResponse)
def create_user(
    request: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        name = request.name,
        email = request.email,
        password_hash = hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "user created successfully!",
        "id" : new_user.id
    }

# ユーザー編集
@router.put("/", response_model = UserUpdateResponse)
def update_user(
    request: UserUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
    )

    user.name = request.name
    user.email = request.email
    db.commit()

    return {
        "message": "user update successfully!",
        "name": user.name, 
        "email": user.email
    }

# ユーザー削除
@router.delete("/", response_model = UserDeleteResponse)
def delete_user(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
        status_code = 404,
        detail = "User not found"
    )

    db.delete(user)
    db.commit()

    return {
    "message": "user delete successfully!",
    "id": user_id
    }

# ログイン
@router.post("/login", response_model = LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db:Session = Depends(get_db)
    ):
    stmt = select(User).where(User.email == form_data.username)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
        status_code = 401,
        detail = "Invalid email or password"
    )

    auth = verify_password(form_data.password, user.password_hash)

    if auth is False:
        raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
        )
    # 認証成功したらトークン作成
    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ログアウト
@router.post("/logout")
def logout():
    # フロント側でaccess_tokenを削除
    return {
        "message": "logout successfully!"
    }