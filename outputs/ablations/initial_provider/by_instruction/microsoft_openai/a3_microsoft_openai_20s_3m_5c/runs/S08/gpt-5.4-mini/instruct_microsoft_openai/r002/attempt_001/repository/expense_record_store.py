import os

from openai import OpenAI


def expense_record_store(record):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Persist the expense record by returning a storage-ready JSON document."},
            {"role": "user", "content": str(record)},
        ],
    )
    return response.output_text
