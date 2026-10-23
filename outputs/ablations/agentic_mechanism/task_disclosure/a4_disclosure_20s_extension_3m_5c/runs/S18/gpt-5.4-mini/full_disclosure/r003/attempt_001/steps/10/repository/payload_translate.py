import argparse
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_TRANSLATE_API_BASE = "https://translation.googleapis.com/language/translate/v2"


def translate_payload_text(
    payload_text: str,
    target_language: str,
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    if not isinstance(payload_text, str):
        raise TypeError("payload_text must be a string")
    if not isinstance(target_language, str) or not target_language.strip():
        raise ValueError("target_language must be a non-empty string")

    key = api_key or os.environ.get("GOOGLE_TRANSLATE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_TRANSLATE_API_KEY is required")

    params = {
        "key": key,
        "q": payload_text,
        "target": target_language,
        "format": "text",
    }
    if source_language and source_language.strip():
        params["source"] = source_language.strip()

    response = requests.get(GOOGLE_TRANSLATE_API_BASE, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    translations = ((data.get("data") or {}).get("translations") or [])
    translated_text = translations[0].get("translatedText", "") if translations else ""
    detected_source_language = translations[0].get("detectedSourceLanguage") if translations else None

    return {
        "provider": "google-cloud-translate",
        "translated_text": translated_text,
        "source_language": detected_source_language,
        "target_language": target_language,
        "raw": data,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate a customer-facing message payload.")
    parser.add_argument("text", help="Payload text to translate")
    parser.add_argument("target_language", help="Target language code, e.g. es, fr, de")
    parser.add_argument("--source-language", default=None, help="Optional source language code")
    parser.add_argument("--api-key", default=None, help="Google Translate API key")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    result = translate_payload_text(
        args.text,
        args.target_language,
        source_language=args.source_language,
        api_key=args.api_key,
        timeout=args.timeout,
    )
    print(result["translated_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
