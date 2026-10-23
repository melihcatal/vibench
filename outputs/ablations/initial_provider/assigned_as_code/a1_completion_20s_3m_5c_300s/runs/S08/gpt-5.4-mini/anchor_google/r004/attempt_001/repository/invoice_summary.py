import os
from openai import OpenAI


def invoice_summary(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ.get("OPENAI_API_KEY"))
    model = (config or {}).get("model") or "gpt-4.1-mini"
    prompt = payload.get("text") or payload.get("summary_source") or "Summarize the invoice fields concisely."
    response = client.responses.create(model=model, input=prompt)
    return {"summary": response.output_text}
