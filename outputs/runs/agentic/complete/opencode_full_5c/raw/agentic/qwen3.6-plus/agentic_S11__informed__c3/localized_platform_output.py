import os
from typing import Optional

from alibabacloud_alimt20181012.client import Client
from alibabacloud_alimt20181012 import models
from alibabacloud_tea_openapi.models import Config

from model_models import TranslationResult


def _build_alimt_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET must be set"
        )
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="mt.cn-hangzhou.aliyuncs.com",
    )
    return Client(config)


LANG_CODE_MAP = {
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


def localized_platform_output(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
) -> TranslationResult:
    client = _build_alimt_client()

    target_code = LANG_CODE_MAP.get(target_lang, target_lang)
    source_code = LANG_CODE_MAP.get(source_lang, source_lang) if source_lang else "auto"

    translate_request = models.TranslateGeneralRequest(
        format_type="text",
        source_text=text,
        source_language=source_code,
        target_language=target_code,
        scene="general",
    )

    response = client.translate_general(translate_request)

    translated = ""
    if response.body and response.body.data:
        translated = response.body.data.translated

    return TranslationResult(
        original_text=text,
        translated_text=translated,
        source_lang=source_code,
        target_lang=target_code,
        provider="Alibaba Machine Translation",
        raw_response=response,
    )


if __name__ == "__main__":
    result = localized_platform_output(
        text="Hello, how are you today?",
        target_lang="zh",
    )
    print("Translated:", result.translated_text)
    print("Provider:", result.provider)
