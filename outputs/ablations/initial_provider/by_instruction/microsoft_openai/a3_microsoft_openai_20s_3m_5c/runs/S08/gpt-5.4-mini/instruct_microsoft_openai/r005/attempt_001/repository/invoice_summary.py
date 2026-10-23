from openai import OpenAI

from document_client import load_config


def invoice_summary(invoice_fields):
    config = load_config()
    client = OpenAI(api_key=config.api_key) if config.api_key else OpenAI()
    prompt = "Summarize the invoice in one concise paragraph from this JSON:\n" + __import__("json").dumps(invoice_fields)
    response = client.responses.create(model=config.model, input=prompt)
    return response.output_text
