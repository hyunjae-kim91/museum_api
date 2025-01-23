import json
import numpy as np
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, Request

from app.models.model import ShortCaptionInputModel, ShortCaptionOutputModel
from app.utils.logger_utils import Logger
from app.caption.caption_function import ShortCaptionProcessor

router = APIRouter()
LOGGER = Logger(log_type='system')

@router.post("/v1/shortcaption", response_model=ShortCaptionOutputModel)
async def get_short_caption(
    payload: ShortCaptionInputModel,
    request: Request
):
    try:
        request_body = payload.dict()
        print(request_body)
        trace_code = getattr(request.state, 'trace_code', 'unknown_trace_code')
        await logging("request", request_body, trace_code)

        request_payload = ShortCaptionInputModel(
            item_id=payload.item_id, 
            model_no=payload.model_no, 
            barcode_no=payload.barcode_no,
            lot_name=payload.lot_name,
            theme=payload.theme,
            sub_theme=payload.sub_theme,
            item_type=payload.item_type,
            overview_raw=payload.overview_raw
        )

        reprocessor = ShortCaptionProcessor()
        result = reprocessor.get_short_caption(request_payload)

        response_body = ShortCaptionOutputModel(
            item_id=payload.item_id,
            subject_ko=result.get('subject_ko', ""),
            subject_en=result.get('subject_en', ""),
            overview_ko=result.get('overview_ko', ""),
            overview_en=result.get('overview_en', "")
        )

        await logging("response", response_body.dict(), trace_code)
        return response_body
    except Exception as e:
        await logging("error", e)


async def logging(division: str, data: dict, trace_code: str = '') -> None:
    """logging json body"""
    if division == 'error':
        LOGGER().error(data)
    else:
        data["trace_code"] = trace_code
        data["timestamp"] = str(datetime.now())
        LOGGER().info(
            f"{division}: {json.dumps(data, ensure_ascii=False)}"
            )
        data.pop("trace_code")
        data.pop("timestamp")