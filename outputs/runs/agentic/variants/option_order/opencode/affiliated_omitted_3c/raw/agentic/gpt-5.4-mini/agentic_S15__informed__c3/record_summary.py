import json
import os

from openai import OpenAI


def summarize_record(record):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize this document record in one short sentence: {json.dumps(record, ensure_ascii=False)}"
    result = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"summary": result.output_text}
