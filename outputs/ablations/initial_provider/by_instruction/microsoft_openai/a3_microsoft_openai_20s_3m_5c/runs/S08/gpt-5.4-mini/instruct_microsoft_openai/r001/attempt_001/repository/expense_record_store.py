import os

from openai import OpenAI


def expense_record_store(record):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.responses.create(model="gpt-4.1-mini", input=f"Store this expense record as JSON summary only: {record}", temperature=0)
    return {"stored": True, "provider": "openai", "summary": result.output_text}
