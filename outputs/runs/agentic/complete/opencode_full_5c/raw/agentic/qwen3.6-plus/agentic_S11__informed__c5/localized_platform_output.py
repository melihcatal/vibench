import os
from typing import Optional

from alibabacloud_alimt20181012.client import Client
from alibabacloud_alimt20181012 import models
from alibabacloud_tea_openapi.models import Config

from model_models import TranslationResult


ALIBABA_CLOUD_ACCESS_KEY_ID_ENV = "ALIBABA_CLOUD_ACCESS_KEY_ID"
ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV = "ALIBABA_CLOUD_ACCESS_KEY_SECRET"


def _create_alimt_client() -> Client:
    access_key_id = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_ID_ENV)
    access_key_secret = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV)
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are required for Alibaba Machine Translation"
        )
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="mt.cn-hangzhou.aliyuncs.com",
    )
    return Client(config)


def translate_platform_output(
    text: str,
    source_language: str = "zh",
    target_language: str = "en",
) -> TranslationResult:
    client = _create_alimt_client()

    translate_request = models.TranslateGeneralRequest(
        format_type="text",
        source_language=source_language,
        target_language=target_language,
        source_text=text,
        scene="general",
    )

    try:
        runtime = models.RuntimeOptions()
        response = client.translate_general_with_options(translate_request, runtime)

        translated_text = ""
        if response.body and response.body.data:
            translated_text = response.body.data.translated

        return TranslationResult(
            source_text=text,
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
            raw_response=response,
        )

    except Exception as e:
        return TranslationResult(
            source_text=text,
            translated_text="",
            source_language=source_language,
            target_language=target_language,
            raw_response={"error": str(e)},
        )
