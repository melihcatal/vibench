from __future__ import annotations

from security_client import translate_client


def runbook_translate(
    text: str,
    target_language_code: str,
    source_language_code: str = "auto",
    region_name: str | None = None,
) -> dict:
    client = translate_client(region_name)
    params = {
        "Text": text,
        "TargetLanguageCode": target_language_code,
    }
    if source_language_code != "auto":
        params["SourceLanguageCode"] = source_language_code
    response = client.translate_text(**params)
    return {
        "provider": "Amazon Translate",
        "translated_text": response["TranslatedText"],
        "source_language_code": response.get(
            "SourceLanguageCode", source_language_code
        ),
        "target_language_code": response["TargetLanguageCode"],
    }
