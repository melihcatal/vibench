import os

import boto3


def get_translation_config(config=None):
    merged = dict(config or {})
    if "region" not in merged:
        merged["region"] = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return merged


def get_translate_client(config=None):
    cfg = get_translation_config(config)
    return boto3.client("translate", region_name=cfg.get("region"))


def translate_text_value(client, text, source_language, target_language):
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]


def translate_text_with_config(text, source_language, target_language, config=None):
    client = get_translate_client(config)
    return translate_text_value(client, text, source_language, target_language)
