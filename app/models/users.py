"""
目的:
    usersテーブルを定義する。
"""

from datetime import datetime

from sqlalchemy import Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    """
    usersテーブル

    目的:
        ユーザー情報を管理する。
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    record: Mapped[list["Record"]] = relationship(back_populates="user")
    category: Mapped[list["Category"]] = relationship(back_populates="user")