import os
from typing import Dict

from openai import OpenAI

TRANSLATION_MODEL_ID = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")


def invoice_note_translate(text: str) -> Dict[str, str]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model=TRANSLATION_MODEL_ID, input=f"Translate the following invoice note to {TARGET_LANGUAGE}: {text}")
    return {"provider": "openai", "model": TRANSLATION_MODEL_ID, "translated_text": response.output_text}
