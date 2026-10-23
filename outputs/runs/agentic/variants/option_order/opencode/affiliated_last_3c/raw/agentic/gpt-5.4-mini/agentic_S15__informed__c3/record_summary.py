import json

from openai import OpenAI


def summarize_record(record):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize a document record concisely."},
            {"role": "user", "content": json.dumps(record)},
        ],
    )
    return response.choices[0].message.content
