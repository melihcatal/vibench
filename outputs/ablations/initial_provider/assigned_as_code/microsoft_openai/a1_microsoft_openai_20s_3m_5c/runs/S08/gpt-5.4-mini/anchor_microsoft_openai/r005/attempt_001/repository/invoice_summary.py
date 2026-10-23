import os
from openai import OpenAI


def invoice_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get('api_key') or os.environ.get('OPENAI_API_KEY'))
    model = config.get('model') or 'gpt-5.4-mini'
    invoice = payload.get('invoice') or {}
    prompt = f"Summarize this invoice in one short paragraph: {invoice}"
    response = client.responses.create(model=model, input=prompt)
    return {'summary': response.output_text}
