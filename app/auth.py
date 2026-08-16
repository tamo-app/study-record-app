from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
import os

# ログイン関係

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    パスワードをハッシュ化する。
    入力: 平文パスワード
    出力: ハッシュ化されたパスワード
    副作用: なし
    """
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    入力されたパスワードが保存済みハッシュと一致するか確認する。
    入力: 平文パスワード、DBに保存されたハッシュ
    出力: 一致すればTrue、不一致ならFalse
    副作用: なし
    """
    return password_hash.verify(password, hashed_password)

# トークン関係

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def create_access_token(user_id: int):
    """
    ログイン時のトークン発行処理
    入力: user_id
    出力: トークン
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    data = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def verify_access_token(token: str):
    """
    アクセストークンを検証し、ユーザーIDを取得する。
    入力: アクセストークン
    出力: ユーザーID
    副作用: 不正なトークンの場合はHTTPExceptionを発生させる
    """
    try:
        pay_load = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = int(pay_load["sub"])

    return user_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
def get_current_user(
        token:str  = Depends(oauth2_scheme)
):
    """
    HTTPリクエストからアクセストークンを取得し、認証済みユーザーのIDを取得する。
    入力: HTTPリクエストのアクセストークン
    出力: ユーザーID
    副作用: 不正なトークンの場合はHTTPExceptionを発生させる
    前提条件: AuthorizationヘッダーにBearerトークンが含まれている
    """
    user_id = verify_access_token(token)

    return user_id