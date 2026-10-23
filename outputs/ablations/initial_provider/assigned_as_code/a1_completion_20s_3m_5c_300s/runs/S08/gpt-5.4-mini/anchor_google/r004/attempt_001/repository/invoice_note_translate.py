import os
from openai import OpenAI


def invoice_note_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ.get("OPENAI_API_KEY"))
    model = (config or {}).get("model") or "gpt-4.1-mini"
    target_language = payload.get("target_language", "English")
    text = payload.get("text", "")
    response = client.responses.create(model=model, input=f"Translate this invoice note into {target_language}: {text}")
    return {"translation": response.output_text}
