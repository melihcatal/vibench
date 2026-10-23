import os
from typing import Optional

from alibabacloud_alimt20181012.client import Client
from alibabacloud_alimt20181012 import models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from model_models import TranslationResult


def _get_alimt_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET "
            "environment variables are required for Alibaba Machine Translation"
        )
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="mt.cn-hangzhou.aliyuncs.com",
    )
    return Client(config)


def translate_platform_output(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    format_type: str = "text",
) -> TranslationResult:
    client = _get_alimt_client()
    source_lang = source_language if source_language != "auto" else "auto"
    translate_request = models.TranslateGeneralRequest(
        format_type=format_type,
        source_language=source_lang,
        target_language=target_language,
        text=text,
        scene="general",
    )
    runtime = util_models.RuntimeOptions()
    response = client.translate_general_with_options(translate_request, runtime)
    translated_text = ""
    request_id = ""
    if hasattr(response, "body") and response.body:
        body = response.body
        request_id = getattr(body, "request_id", "")
        if hasattr(body, "data") and body.data:
            translated_text = getattr(body.data, "translated", "")
    return TranslationResult(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        request_id=request_id,
        model_id="alimt-general",
    )


def translate_platform_output_batch(
    texts: list,
    source_language: str = "auto",
    target_language: str = "en",
) -> list:
    results = []
    for text in texts:
        result = translate_platform_output(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
        results.append(result)
    return results
