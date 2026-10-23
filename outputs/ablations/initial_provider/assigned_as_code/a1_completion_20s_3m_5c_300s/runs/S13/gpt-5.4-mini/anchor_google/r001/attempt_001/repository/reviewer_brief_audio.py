import os

from openai import OpenAI


def reviewer_brief_audio(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ["OPENAI_API_KEY"])
    model = (config or {}).get("model", "gpt-4o-mini-tts")
    response = client.audio.speech.create(model=model, voice=(config or {}).get("voice", "alloy"), input=payload["text"])
    return {"audio": response.content, "model": model}
