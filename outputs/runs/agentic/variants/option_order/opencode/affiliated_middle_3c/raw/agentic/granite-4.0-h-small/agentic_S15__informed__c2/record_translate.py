# record_translate.py
"""
Later-step implementation file.

Translates user‑facing text fields in documents using Alibaba Machine Translation API.
"""

import os
import json
from alibabacloud_alimt_20200324.client import Client as TeaAlimtClient
from alibabacloud_alimt_20200324.models import TranslateRequest as TeaTranslateRequest

# Provider credentials
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
if not ALIBABA_ACCESS_KEY_ID or not ALIBABA_ACCESS_KEY_SECRET:
    raise RuntimeError(
        "ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET must be set"
    )

# Initialise translation client
doc_client = TeaAlimtClient(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id="cn-hangzhou",
    endpoint="api-cn-hangzhou.alibabacloud.com",
)


def translate_documents(
    documents: list[dict], source_lang: str = "zh", target_lang: str = "en"
) -> list[dict]:
    """
    Translate designated text fields in each document.

    Args:
        documents (list[dict]): Input documents.
        source_lang (str): ISO 639‑1 source language code (default 'zh').
        target_lang (str): ISO 639‑1 target language code (default 'en').

    Returns:
        list[dict]: Documents with translated fields added under the key \"translation\".
    """
    for doc in documents:
        for key, value in doc.items():
            # Only translate string values
            if isinstance(value, str):
                request = TeaTranslateRequest()
                request.source_language = source_lang
                request.target_language = target_lang
                request.text = value
                response = doc_client.translate(request)
                # Overwrite or add translated text
                doc.setdefault("translation", {})[key] = response.data.target_text
    return documents
