from __future__ import annotations

import os
from typing import Any, Dict, Optional

from alibabacloud_alimt20181012.client import Client
from alibabacloud_alimt20181012 import models as alimt_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from model_models import TranslationResult


ALIBABA_CLOUD_ACCESS_KEY_ID_ENV = "ALIBABA_CLOUD_ACCESS_KEY_ID"
ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV = "ALIBABA_CLOUD_ACCESS_KEY_SECRET"
ALIMT_ENDPOINT = "mt.cn-hangzhou.aliyuncs.com"

LANGUAGE_CODES = {
    "en": "en",
    "zh": "zh",
    "ja": "ja",
    "ko": "ko",
    "fr": "fr",
    "de": "de",
    "es": "es",
    "ru": "ru",
    "ar": "ar",
    "pt": "pt",
}


def _get_credentials() -> tuple:
    access_key_id = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_ID_ENV)
    access_key_secret = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV)
    if not access_key_id or not access_key_secret:
        raise ValueError(
            f"Environment variables {ALIBABA_CLOUD_ACCESS_KEY_ID_ENV} and "
            f"{ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV} are required for Alibaba Machine Translation"
        )
    return access_key_id, access_key_secret


def _create_client() -> Client:
    access_key_id, access_key_secret = _get_credentials()
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=ALIMT_ENDPOINT,
    )
    return Client(config)


def translate_platform_output(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    scene: str = "general",
) -> TranslationResult:
    client = _create_client()

    source_lang = LANGUAGE_CODES.get(source_language, source_language)
    target_lang = LANGUAGE_CODES.get(target_language, target_language)

    request = alimt_models.TranslateGeneralRequest(
        format_type="text",
        source_language=source_lang,
        target_language=target_lang,
        source_text=text,
        scene=scene,
    )

    runtime = util_models.RuntimeOptions()
    response = client.translate_general_with_options(request, runtime)

    translated = ""
    if response.body and response.body.data:
        translated = (
            response.body.data.translated
            if hasattr(response.body.data, "translated")
            else response.body.data.get("translated", "")
        )

    return TranslationResult(
        translated_text=translated,
        source_language=source_lang,
        target_language=target_lang,
        raw_response=response,
    )


def translate_batch(
    texts: list,
    source_language: str = "auto",
    target_language: str = "en",
    scene: str = "general",
) -> list:
    client = _create_client()

    source_lang = LANGUAGE_CODES.get(source_language, source_language)
    target_lang = LANGUAGE_CODES.get(target_language, target_language)

    results = []
    for text in texts:
        request = alimt_models.TranslateGeneralRequest(
            format_type="text",
            source_language=source_lang,
            target_language=target_lang,
            source_text=text,
            scene=scene,
        )
        runtime = util_models.RuntimeOptions()
        response = client.translate_general_with_options(request, runtime)

        translated = ""
        if response.body and response.body.data:
            translated = (
                response.body.data.translated
                if hasattr(response.body.data, "translated")
                else response.body.data.get("translated", "")
            )

        results.append(
            TranslationResult(
                translated_text=translated,
                source_language=source_lang,
                target_language=target_lang,
                raw_response=response,
            )
        )

    return results
