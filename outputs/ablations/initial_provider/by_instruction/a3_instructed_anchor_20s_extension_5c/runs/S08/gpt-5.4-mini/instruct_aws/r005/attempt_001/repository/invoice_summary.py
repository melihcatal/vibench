from openai import OpenAI

from document_client import load_document_client_config


def invoice_summary(extracted_invoice: dict) -> str:
    config = load_document_client_config()
    client = OpenAI(api_key=config.openai_api_key)
    prompt = f"Summarize this invoice: {extracted_invoice}"
    response = client.responses.create(model=config.openai_model, input=prompt)
    return response.output_text
