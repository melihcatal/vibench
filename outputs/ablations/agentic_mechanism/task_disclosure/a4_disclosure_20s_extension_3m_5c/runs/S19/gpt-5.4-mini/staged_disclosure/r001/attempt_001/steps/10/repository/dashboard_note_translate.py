import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
import requests


DEEPL_API_BASE = "https://api-free.deepl.com/v2/translate"


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None


def _normalize_locale(locale: str) -> str:
    value = (locale or "").strip().lower().replace("_", "-")
    return value


def _extract_text(payload: Dict[str, Any]) -> str:
    if "note" in payload and isinstance(payload["note"], str):
        return payload["note"]
    if "text" in payload and isinstance(payload["text"], str):
        return payload["text"]
    if "message" in payload and isinstance(payload["message"], str):
        return payload["message"]
    raise ValueError("Payload must include note, text, or message")


def translate_dashboard_note(payload: Dict[str, Any], target_locale: str) -> Dict[str, Any]:
    text = _extract_text(payload)
    target = _normalize_locale(target_locale)
    deepl_target = target.split("-")[0].upper()

    api_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise EnvironmentError("DEEPL_AUTH_KEY or DEEPL_API_KEY is required")

    response = requests.post(
        DEEPL_API_BASE,
        data={"auth_key": api_key, "text": text, "target_lang": deepl_target},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    if not translations:
        raise ValueError("DeepL response did not include translations")

    translated = translations[0].get("text", "")
    detected = translations[0].get("detected_source_language")
    result = TranslationResult(translated_text=translated, detected_source_language=detected)

    output = dict(payload)
    output["translated_note"] = result.translated_text
    output["translated_locale"] = target
    if result.detected_source_language:
        output["source_language"] = result.detected_source_language.lower()
    return output


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate a dashboard note using DeepL")
    parser.add_argument("--payload", required=True, help="JSON payload containing note/text/message")
    parser.add_argument("--target-locale", required=True, help="Target locale, e.g. fr-FR")
    args = parser.parse_args()

    payload = json.loads(args.payload)
    result = translate_dashboard_note(payload, args.target_locale)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
