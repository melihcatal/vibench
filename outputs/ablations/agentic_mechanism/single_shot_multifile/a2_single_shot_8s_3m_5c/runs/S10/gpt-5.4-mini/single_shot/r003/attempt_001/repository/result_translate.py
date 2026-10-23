from openai import OpenAI
from model_client import get_text_client, resolve_text_model
from model_models import normalize_text_result


def result_translate(text: str, target_language: str, model: str | None = None) -> str:
    client = get_text_client()
    model_name = resolve_text_model(model, task="translate")
    prompt = f"Translate the following text into {target_language}. Preserve meaning and formatting.\n\n{text}"
    response = client.responses.create(model=model_name, input=prompt)
    return normalize_text_result(response)
