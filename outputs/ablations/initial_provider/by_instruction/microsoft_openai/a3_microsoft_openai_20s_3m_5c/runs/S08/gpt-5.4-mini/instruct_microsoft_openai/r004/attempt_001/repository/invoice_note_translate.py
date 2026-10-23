import os

from openai import OpenAI


def invoice_note_translate(text, target_language="en"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), input=[{"role": "user", "content": f"Translate to {target_language}: {text}"}])
    return {"translated_text": response.output_text}
