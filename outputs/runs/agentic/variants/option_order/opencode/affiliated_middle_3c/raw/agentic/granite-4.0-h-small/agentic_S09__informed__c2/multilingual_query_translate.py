# multilingual_query_translate.py - LATER-STEP
# Translate queries to the target language before multilingual embedding search

import os
from typing import List

# Example provider: Alibaba Cloud Machine Translation SDK
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
if not (ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET):
    raise ValueError(
        "Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    )

from alibabacloud_alimt20181011 import client as alimt_client
from alibabacloud_tea_openapi import models as open_api_models

_client = None


def _get_mt_client() -> alimt_client.AlimtClient:
    """Lazy initialize Alibaba Machine Translation client."""
    global _client
    if _client is None:
        _client = alimt_client.AlimtClient(
            endpoint="mt.cn-shanghai.aliyuncs.com",
            access_key_id=ALIBABA_ACCESS_KEY_ID,
            access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
        )
    return _client


def translate_queries(
    queries: List[str], source_lang: str = "zh", target_lang: str = "en"
) -> List[str]:
    """
    Translate a list of queries from source_lang to target_lang.

    Returns translated queries preserving order.
    """
    client = _get_mt_client()
    request = {
        "SourceLanguage": source_lang,
        "TargetLanguage": target_lang,
        "SourceText": "\n".join(queries),
    }
    response = client.translate(request)
    # Assuming response returns a JSON list of translated strings
    # Adjust based on actual SDK response format
    return response.get("Translated", [])
