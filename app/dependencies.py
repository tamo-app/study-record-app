"""
目的:
    FastAPIへSessionを提供する。
入力:
    なし
出力:
    Session
副作用:
    Sessionを開閉する。
前提条件:
    SessionLocalが作成されていること。
"""

from collections.abc import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    目的:
        APIごとにSessionを生成し、処理終了後に必ず閉じる。
    入力:
        なし
    出力:
        Session
    副作用:
        Sessionを生成・破棄する。
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()