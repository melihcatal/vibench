from typing import Any, Dict, Optional
from openai import OpenAI
from safety_client import build_openai_client, provider_name

MODEL = "gpt-4o-mini"


def appeal_translate(text: str, target_language: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    prompt = f"Translate this moderation appeal into {target_language} while preserving tone and meaning:\n{text}"
    response = client.responses.create(model=MODEL, input=prompt)
    translated = getattr(response, "output_text", None) or str(response)
    return {
        "provider": provider_name(),
        "operation": "appeal_translate",
        "model": MODEL,
        "target_language": target_language,
        "source_text": text,
        "translated_text": translated,
        "metadata": metadata or {},
    }
