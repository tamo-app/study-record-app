"""
目的:
    User APIのリクエスト・レスポンスの型を定義する
"""

from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    ユーザー作成のリクエスト
    """
    name: str
    email: str
    password: str

class UserCreateResponse(BaseModel):
    """
    ユーザー作成のレスポンス
    """
    id: int
    message: str

class UserDetailResponse(BaseModel):
    """
    ユーザー詳細取得のレスポンス
    """
    message: str
    id: int
    name: str
    email: str
    
class UserUpdate(BaseModel):
    """
    ユーザー情報更新時のリクエスト
    """
    name: str
    email: str

class UserUpdateResponse(BaseModel):
    """
    ユーザー情報更新のレスポンス
    """
    message: str
    name: str
    email: str

class UserDeleteResponse(BaseModel):
    """
    ユーザー削除のレスポンス
    """
    message: str
    id: int

class LoginResponse(BaseModel):
    """
    ログイン成功時のレスポンス
    """
    access_token: str
    token_type: str