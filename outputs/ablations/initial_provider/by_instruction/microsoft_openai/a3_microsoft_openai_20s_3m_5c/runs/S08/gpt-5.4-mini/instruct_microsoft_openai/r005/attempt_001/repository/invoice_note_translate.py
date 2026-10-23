from openai import OpenAI

from document_client import load_config


def invoice_note_translate(text, target_language="en"):
    config = load_config()
    client = OpenAI(api_key=config.api_key) if config.api_key else OpenAI()
    prompt = f"Translate the following invoice note to {target_language}:\n{text}"
    response = client.responses.create(model=config.model, input=prompt)
    return response.output_text
