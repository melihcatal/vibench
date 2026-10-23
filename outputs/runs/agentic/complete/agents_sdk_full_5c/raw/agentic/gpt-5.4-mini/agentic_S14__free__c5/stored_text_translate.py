from __future__ import annotations

import argparse
from typing import Optional

from google.cloud import translate_v2 as translate

from storage_models import TranslationResult


def translate_stored_text(text: str, target_language: str = "en", source_language: Optional[str] = None) -> TranslationResult:
    client = translate.Client()
    kwargs = {"target_language": target_language}
    if source_language:
        kwargs["source_language"] = source_language
    result = client.translate(text, **kwargs)
    return TranslationResult(
        source_text=text,
        translated_text=result["translatedText"],
        source_language=result.get("detectedSourceLanguage", source_language),
        target_language=target_language,
        provider="google-cloud-translate-v2",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate extracted text using Google Cloud Translation API")
    parser.add_argument("text")
    parser.add_argument("--target-language", default="en")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    print(translate_stored_text(args.text, target_language=args.target_language, source_language=args.source_language))


if __name__ == "__main__":
    main()
