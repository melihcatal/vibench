"""
Translate user-facing document fields using Amazon Translate.
"""

import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
TARGET_LANGUAGE_CODE = os.environ.get("TARGET_LANGUAGE_CODE", "en")


def get_translate_client():
    """Return a boto3 Amazon Translate client."""
    return boto3.client("translate", region_name=AWS_REGION)


def translate_text(text: str, target_lang: str | None = None) -> dict:
    """
    Translate a single text string using Amazon Translate.

    Parameters
    ----------
    text : str
        Source text to translate.
    target_lang : str, optional
        Target language code (e.g. ``"en"``).  Defaults to ``TARGET_LANGUAGE_CODE``.

    Returns
    -------
    dict
        Keys: ``translated_text``, ``source_language_code``, ``target_language_code``.
    """
    client = get_translate_client()
    tgt = target_lang or TARGET_LANGUAGE_CODE

    try:
        response = client.translate_text(
            Text=text,
            TargetLanguageCode=tgt,
        )
        return {
            "translated_text": response["TranslatedText"],
            "source_language_code": response["SourceLanguageCode"],
            "target_language_code": tgt,
        }
    except (BotoCoreError, ClientError) as exc:
        return {
            "translated_text": None,
            "source_language_code": None,
            "target_language_code": tgt,
            "error": str(exc),
        }


def translate_document_fields(
    document: dict,
    fields: list[str] | None = None,
    target_lang: str | None = None,
) -> dict:
    """
    Translate selected string fields in a document via Amazon Translate.

    Parameters
    ----------
    document : dict
        The source document record.
    fields : list[str], optional
        Specific field names to translate.  If ``None``, all string fields are translated.
    target_lang : str, optional
        Target language code.

    Returns
    -------
    dict
        A new dict with translated fields added under a ``_translations`` key
        and original fields preserved.
    """
    result = dict(document)
    translations = {}

    keys = fields or [k for k, v in document.items() if isinstance(v, str)]

    for key in keys:
        value = document.get(key)
        if isinstance(value, str) and value.strip():
            translations[key] = translate_text(value, target_lang)

    result["_translations"] = translations
    return result
