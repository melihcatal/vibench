import os
from typing import Optional

from alibabacloud_alimt20181012.client import Client
from alibabacloud_alimt20181012 import models as alimt_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from model_models import TranslationResult

ALIBABA_TRANSLATE_ENDPOINT = "mt.cn-hangzhou.aliyuncs.com"


def _build_alibaba_translate_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise RuntimeError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET "
            "environment variables are required for Alibaba Machine Translation"
        )
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=ALIBABA_TRANSLATE_ENDPOINT,
    )
    return Client(config)


def translate_platform_output(
    text: str,
    source_language: str = "zh",
    target_language: str = "en",
    format_type: str = "text",
    scene: str = "general",
) -> TranslationResult:
    client = _build_alibaba_translate_client()

    request = alimt_models.TranslateGeneralRequest(
        format_type=format_type,
        source_language=source_language,
        target_language=target_language,
        text=text,
        scene=scene,
    )

    runtime = util_models.RuntimeOptions()
    response = client.translate_general_with_options(request, runtime)

    body = response.body
    translated = ""
    if body and hasattr(body, "data") and body.data:
        translated = getattr(body.data, "translated", "")

    return TranslationResult(
        translated_text=translated,
        source_language=source_language,
        target_language=target_language,
        raw_response=response,
    )


def localize_platform_output(
    text: str,
    target_locale: str = "en-US",
    source_locale: Optional[str] = None,
) -> TranslationResult:
    locale_to_lang = {
        "en-US": "en",
        "en-GB": "en",
        "zh-CN": "zh",
        "zh-TW": "zh",
        "ja-JP": "ja",
        "ko-KR": "ko",
        "fr-FR": "fr",
        "de-DE": "de",
        "es-ES": "es",
        "ru-RU": "ru",
        "ar-SA": "ar",
        "pt-BR": "pt",
    }

    target_lang = locale_to_lang.get(target_locale, target_locale)

    if source_locale:
        source_lang = locale_to_lang.get(source_locale, source_locale)
    else:
        source_lang = "auto"

    return translate_platform_output(
        text=text,
        source_language=source_lang,
        target_language=target_lang,
    )
