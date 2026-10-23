from openai import OpenAI
from model_client import get_text_client, resolve_audio_model, resolve_text_model
from model_models import normalize_text_result


def spoken_brief(text: str, model: str | None = None) -> str:
    client = get_text_client()
    model_name = resolve_text_model(model or resolve_audio_model(None), task="speech")
    prompt = f"Rewrite the following into a short spoken brief suitable for audio narration.\n\n{text}"
    response = client.responses.create(model=model_name, input=prompt)
    return normalize_text_result(response)
