"""
目的:
    categoriesテーブルを定義する。
"""

from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    """
    categoriesテーブル

    目的:
        学習カテゴリを管理する。
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    detail: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime | None] = mapped_column(DateTime)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    user: Mapped["User"] = relationship(back_populates="category")
    record: Mapped[list["Record"]] = relationship(back_populates="category")