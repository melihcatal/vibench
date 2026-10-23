from typing import Any, Dict
from openai import OpenAI
from safety_client import get_openai_client

TRANSLATION_MODEL = "gpt-4.1-mini"


def appeal_translate(text: str, target_language: str = "en", *, model: str | None = None) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    chosen_model = model or TRANSLATION_MODEL
    prompt = f"Translate the following appeal text into {target_language} while preserving meaning and tone:\n{text}"
    response = client.responses.create(model=chosen_model, input=prompt)
    return {"translation": response.output_text, "target_language": target_language, "model": chosen_model}


if __name__ == "__main__":
    raise SystemExit(0)
