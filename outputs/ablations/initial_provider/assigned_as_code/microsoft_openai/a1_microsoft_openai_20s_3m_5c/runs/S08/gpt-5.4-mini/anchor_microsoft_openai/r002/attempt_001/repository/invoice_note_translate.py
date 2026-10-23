import os

from openai import OpenAI


def invoice_note_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"))
    note = payload.get("note") or payload.get("text") or ""
    target_language = config.get("target_language") or payload.get("target_language") or "en"
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following invoice note to {target_language}: {note}",
    )
    return {"translated_note": response.output_text}
