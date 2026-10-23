from __future__ import annotations

import argparse

from storage_client import get_translate_client, load_settings
from storage_models import TranslationResult


def translate_stored_text(source_text: str, target_language: str = "en", source_language: str = "auto") -> TranslationResult:
    translate = get_translate_client()
    kwargs = {"Text": source_text, "TargetLanguageCode": target_language}
    if source_language != "auto":
        kwargs["SourceLanguageCode"] = source_language
    response = translate.translate_text(**kwargs)
    return TranslationResult(
        source_text=source_text,
        target_language=target_language,
        translated_text=response.get("TranslatedText", ""),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--target-language", default="en")
    args = parser.parse_args()
    _ = load_settings()
    print(translate_stored_text(args.text, args.target_language))
