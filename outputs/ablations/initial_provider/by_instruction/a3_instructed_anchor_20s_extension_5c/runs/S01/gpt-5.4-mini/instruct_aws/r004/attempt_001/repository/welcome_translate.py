from typing import Any, Dict

from openai import OpenAI

from identity_models import normalize_locale


def welcome_translate(copy: str, locale: str) -> Dict[str, Any]:
    client = OpenAI()
    normalized = normalize_locale(locale)
    resp = client.responses.create(model="gpt-5.4-mini", input=f"Translate the following onboarding copy into {normalized}: {copy}")
    return {"locale": normalized, "translation": resp.output_text}


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    event = event or {}
    return welcome_translate(event["copy"], event["locale"])
