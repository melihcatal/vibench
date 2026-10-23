from openai import OpenAI
from model_client import get_text_client, resolve_text_model
from model_models import normalize_text_result


def summarize_text(text: str, max_words: int = 120, model: str | None = None) -> str:
    client = get_text_client()
    model_name = resolve_text_model(model, task="summarize")
    prompt = f"Summarize the following text in about {max_words} words.\n\n{text}"
    response = client.responses.create(model=model_name, input=prompt)
    return normalize_text_result(response)
