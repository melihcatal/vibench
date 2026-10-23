from openai import OpenAI

from document_client import get_api_key, get_model


def vendor_text_safety(text: str):
    client = OpenAI(api_key=get_api_key() or None)
    resp = client.responses.create(
        model=get_model(),
        input=f"Moderate vendor notes or memo fields for safety: {text}",
    )
    return resp.output_text
