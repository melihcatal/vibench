from __future__ import annotations

import os

import boto3


TRANSLATE_CLIENT = boto3.client("translate")


def translate_script(text: str, source_lang: str, target_lang: str) -> str:
    resp = TRANSLATE_CLIENT.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )
    return resp["TranslatedText"]
