# [LATER-STEP] runbook_translate.py
# Translate secret-rotation runbook notes using Alibaba Cloud Machine Translation SDK

import os
import alibabacloud_alimt20230331 as alimt
from alibabacloud_tea_openapi20200326 import models as open_api_models
from alibabacloud_tea_util20200304 import models as util_models
from fetch_api_key import fetch_api_key


def translate_runbook(note: str, target_lang: str = "en") -> str:
    """Translate a runbook note to the target language using Alibaba MT."""
    client = alimt.Client(
        open_api_models.Config(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            endpoint="mt.cn-shanghai.aliyuncs.com",
        )
    )
    request = alimt.TranslateTextRequest(
        SourceLanguage="auto", TargetLanguage=target_lang, SourceText=note
    )
    response = client.translate_text(request)
    return response.body.targetText
