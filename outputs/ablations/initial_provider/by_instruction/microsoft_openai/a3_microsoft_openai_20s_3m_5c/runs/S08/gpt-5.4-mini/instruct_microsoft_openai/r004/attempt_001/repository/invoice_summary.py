import os

from openai import OpenAI


def invoice_summary(data):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), input=[{"role": "user", "content": str(data)}])
    return {"summary": response.output_text}
