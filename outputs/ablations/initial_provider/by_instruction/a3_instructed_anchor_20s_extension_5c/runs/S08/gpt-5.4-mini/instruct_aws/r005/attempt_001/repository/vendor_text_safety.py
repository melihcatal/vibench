from openai import OpenAI

from document_client import load_document_client_config


def vendor_text_safety(text: str) -> dict:
    config = load_document_client_config()
    client = OpenAI(api_key=config.openai_api_key)
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.model_dump()
