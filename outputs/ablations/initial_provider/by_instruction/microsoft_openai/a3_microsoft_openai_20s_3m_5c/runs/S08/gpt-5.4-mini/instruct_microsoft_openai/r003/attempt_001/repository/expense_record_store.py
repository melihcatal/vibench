import os

from openai import OpenAI


def expense_record_store(record):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return client.responses.create(model="gpt-5.4-mini", input=str(record))
