from openai import OpenAI

from document_client import get_api_key, get_model


def invoice_summary(extracted: dict):
    client = OpenAI(api_key=get_api_key() or None)
    resp = client.responses.create(
        model=get_model(),
        input=f"Summarize this extracted invoice fields payload: {extracted}",
    )
    return resp.output_text
