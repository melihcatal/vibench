from openai import OpenAI


def invoice_note_translate(text, target_language="en"):
    client = OpenAI(api_key=None)
    return client.responses.create(model="gpt-5.4-mini", input=f"Translate to {target_language}: {text}").output_text
