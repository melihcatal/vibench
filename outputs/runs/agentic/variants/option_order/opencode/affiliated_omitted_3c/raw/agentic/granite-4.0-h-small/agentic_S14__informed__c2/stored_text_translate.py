# [LATER-STEP] stored_text_translate.py

# Uses Alibaba Cloud Machine Translation API for translating extracted text.
# Provider: Alibaba Cloud Machine Translation
# SDK: alibabacloud_alimt
# Auth: ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET

import os
import json
from alibabacloud_alimt20200630.client import Client
from alibabacloud_alimt20200630.models import TranslateGeneralRequest
from .storage_client import get_bucket_name
from .storage_client import _download_object


# Helper to fetch translation credentials from environment
def _get_alimt_client() -> Client:
    ak_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    ak_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ak_id or not ak_secret:
        raise RuntimeError("Alibaba Cloud credentials not configured")
    return Client(
        access_key_id=ak_id,
        access_key_secret=ak_secret,
        region_id="ap-southeast-1",  # choose appropriate region
    )


# Public entry point
async def translate_text(
    target_lang: str, object_key: str, bucket_name: str = None
) -> dict:
    """Translates extracted raw text from a stored document.

    Args:
        target_lang: BCP-47 language code (e.g., 'en', 'fr', 'es').
        object_key: S3 key of the source document (plain text file).
        bucket_name: Optional bucket; defaults to env var.

    Returns:
        dict with `translatedText`, `srcLang`, `targetLang`, `sourceText`, etc.
    """
    if bucket_name is None:
        bucket_name = get_bucket_name()

    raw_text = _download_object(bucket_name, object_key).decode("utf-8")
    client = _get_alimt_client()
    response = client.translate_general(
        TranslateGeneralRequest(
            SourceText=raw_text,
            SourceLanguage="auto",
            TargetLanguage=target_lang,
        )
    )
    # Response is a protobuf; convert to dict for simplicity
    return {
        "translatedText": response["TranslatedText"],
        "srcLang": response["SourceLanguage"],
        "targetLang": response["TargetLanguage"],
        "sourceText": response["SourceText"],
    }


# Example usage:
# if __name__ == '__main__':
#     print(translate_text('es', 'en_text.txt'))
