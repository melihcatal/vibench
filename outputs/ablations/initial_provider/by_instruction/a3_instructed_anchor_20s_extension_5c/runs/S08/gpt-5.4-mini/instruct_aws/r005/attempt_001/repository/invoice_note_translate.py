from openai import OpenAI

from document_client import load_document_client_config


def invoice_note_translate(text: str, target_language: str = "en") -> str:
    config = load_document_client_config()
    client = OpenAI(api_key=config.openai_api_key)
    response = client.responses.create(
        model=config.openai_model,
        input=f"Translate to {target_language}: {text}",
    )
    return response.output_text
