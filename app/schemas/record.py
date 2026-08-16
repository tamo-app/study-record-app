"""
目的:
    record APIのリクエスト・レスポンスの型を定義する
"""

from pydantic import BaseModel

class SummaryItem(BaseModel):
    """
    学習時間集計の1件分のデータ
    """
    category_name: str
    study_minutes: int

class SummaryResponse(BaseModel):
    """
    学習時間集計取得のレスポンス
    """
    message: str
    summary: list[SummaryItem]
    
class CreateRecord(BaseModel):
    """
    学習記録作成時のリクエスト
    """
    title: str
    category_id: int
    study_minutes: int
    detail: str

class CreateRecordResponse(BaseModel):
    """
    学習記録作成のレスポンス
    """
    message: str
    id: int
    title: str

class RecordListItem(BaseModel):
    """
    学習記録一覧の1件分のデータ
    """
    id: int
    category_name: str
    title: str
    study_minutes: int
    
class GetAllRecordsResponse(BaseModel):
    """
    学習記録一覧取得のレスポンス
    """
    message: str
    records: list[RecordListItem]

class RecordItem(BaseModel):
    """
    学習記録詳細のデータ
    """
    id: int
    category_name: str
    title: str
    study_minutes: int
    detail: str
    
class GetRecordResponse(BaseModel):
    """
    学習記録詳細取得のレスポンス
    """
    message: str
    record: RecordItem

class UpdateRecord(BaseModel):
    """
    学習記録更新時のリクエスト
    """
    category_id: int
    title: str
    study_minutes: int
    detail: str

class UpdateRecordResponse(BaseModel):
    """
    学習記録更新のレスポンス
    """
    message: str
    title: str

class DeleteRecordResponse(BaseModel):
    """
    学習記録削除のレスポンス
    """
    message: str
    record_id: int
