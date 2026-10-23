from openai import OpenAI

from speech_models import normalize_caption_event


def live_caption_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    target_language = payload["target_language"]
    text = payload["text"]
    response = client.responses.create(model=config.get("model", "gpt-4.1-mini"), input=f"Translate the following caption to {target_language}: {text}")
    return normalize_caption_event(response.output_text, is_final=payload.get("is_final", False), target_language=target_language)
