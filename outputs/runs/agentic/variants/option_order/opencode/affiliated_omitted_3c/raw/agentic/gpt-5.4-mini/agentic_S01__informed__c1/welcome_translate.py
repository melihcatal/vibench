import os

from google.cloud import translate_v2 as translate

from identity_models import normalize_locale


def welcome_translate(text: str, locale: str):
    client = translate.Client()
    target = normalize_locale(locale)
    return client.translate(
        text,
        target_language=target,
        source_language=os.environ.get("WELCOME_SOURCE_LANGUAGE", "en"),
    )
