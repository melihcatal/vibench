import os

from openai import OpenAI


def summarize_meeting(chunks: list[str]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = [
        {"role": "system", "content": "Summarize the meeting concisely."},
        {"role": "user", "content": "\n".join(chunks)},
    ]
    resp = client.chat.completions.create(model="gpt-5.4-mini", messages=messages)
    return resp.choices[0].message.content or ""
