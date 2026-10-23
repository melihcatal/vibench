import os
from openai import OpenAI


def message_summary(records: list[dict]):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {"records": records}
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": str(prompt)}]
    )
    return response.choices[0].message.content
