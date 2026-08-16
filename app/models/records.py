"""
目的:
    recordsテーブルを定義する。
"""

from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Record(Base):
    """
    recordsテーブル

    目的:
        学習記録を管理する。
    """

    __tablename__ = "records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    study_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    detail: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime | None] = mapped_column(DateTime)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    user: Mapped["User"] = relationship(back_populates="record")
    category: Mapped["Category"] = relationship(back_populates="record")