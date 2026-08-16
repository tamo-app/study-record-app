"""
目的:
    category APIのリクエスト・レスポンスの型を定義する
"""

from pydantic import BaseModel

class CreateCategory(BaseModel):
    """
    カテゴリ作成時のリクエスト
    """
    name: str
    detail: str

class CreateCategoryResponse(BaseModel):
    """
    カテゴリ作成のレスポンス
    """
    id: int
    message: str

class CategoryListItem(BaseModel):
    """
    カテゴリ一覧の1件分のデータ
    """
    id: int
    name: str
    detail: str

class GetCategoryResponse(BaseModel):
    """
    カテゴリ一覧取得のレスポンス
    """
    message: str
    categories: list[CategoryListItem]

class UpdateCategory(BaseModel):
    """
    カテゴリ更新時のリクエスト
    """
    name: str
    detail: str

class UpdateCategoryResponse(BaseModel):
    """
    カテゴリ更新のレスポンス
    """
    message: str
    category_id: int

class DeleteCategoryResponse(BaseModel):
    """
    カテゴリ削除のレスポンス
    """
    message: str
    category_id: int