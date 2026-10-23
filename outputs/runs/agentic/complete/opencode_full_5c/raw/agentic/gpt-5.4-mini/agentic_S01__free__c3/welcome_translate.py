import os
from typing import Any, Dict

from openai import OpenAI


def welcome_translate(event: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    locale = str(event.get("locale", "en")).strip() or "en"
    copy = str(event.get("copy", "Welcome aboard.")).strip()
    model = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")
    response = client.responses.create(
        model=model, input=f"Translate to {locale}: {copy}"
    )
    return {"locale": locale, "translation": response.output_text}
