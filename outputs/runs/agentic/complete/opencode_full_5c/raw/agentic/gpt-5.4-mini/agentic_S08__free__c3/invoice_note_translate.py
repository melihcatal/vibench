from openai import OpenAI

from document_client import get_api_key, get_model


def invoice_note_translate(text: str, target_language: str):
    client = OpenAI(api_key=get_api_key() or None)
    resp = client.responses.create(
        model=get_model(),
        input=f"Translate this invoice note or description to {target_language}: {text}",
    )
    return resp.output_text
