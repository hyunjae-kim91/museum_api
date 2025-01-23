from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ShortCaptionInputModel(BaseModel):
    """input parameter"""
    item_id: int
    model_no: str
    barcode_no: str
    lot_name: str
    theme: str
    sub_theme: str
    item_type: str
    overview_raw: str

class ShortCaptionOutputModel(BaseModel):
    """전체 응답 모델"""
    item_id: int
    subject_ko: str
    subject_en: str
    overview_ko: str
    overview_en: str
