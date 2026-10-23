from openai import OpenAI


def invoice_note_translate(text, target_language="en"):
    client = OpenAI()
    result = client.responses.create(model="gpt-4.1-mini", input=f"Translate to {target_language}: {text}", temperature=0)
    return result.output_text
