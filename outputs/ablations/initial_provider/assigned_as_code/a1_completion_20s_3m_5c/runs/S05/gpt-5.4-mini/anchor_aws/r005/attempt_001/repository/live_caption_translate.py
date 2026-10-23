import os

from openai import OpenAI

from speech_models import normalize_text


def live_caption_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"))
    target_language = config.get("target_language") or os.environ.get("CAPTION_TARGET_LANGUAGE") or "es"
    text = normalize_text(payload.get("text"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate live captions into {target_language} and preserve meaning.",
            },
            {"role": "user", "content": text},
        ],
    )
    return {"text": response.output_text, "target_language": target_language}
