"""
目的:
    データベース接続を管理する
入力:
    .envのDATABASE_URL
出力:
    Engine, session, Base
前提条件:
    DATABASE_URLが設定されていること

"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# .env を読み込む
load_dotenv()

# 接続URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")

# Engineを作成
engine = create_engine(DATABASE_URL)

# Sessionを作成するための設定
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 全モデル共通の親クラス
class Base(DeclarativeBase):
    pass