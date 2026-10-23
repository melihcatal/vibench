from typing import Dict
from openai import OpenAI
from safety_client import get_openai_client

TRANSLATION_MODEL = "gpt-4.1-mini"


def appeal_translate(text: str, target_language: str = "en", client: OpenAI = None) -> Dict[str, str]:
    client = client or get_openai_client()
    prompt = f"Translate this moderation appeal into {target_language}: {text}"
    resp = client.responses.create(model=TRANSLATION_MODEL, input=prompt)
    return {"translated_text": resp.output_text, "target_language": target_language, "model": TRANSLATION_MODEL}
