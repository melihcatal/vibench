import os

from openai import OpenAI


def summarize_message_results(text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Summarize message processing results: {text}"}
        ],
    )
    return response.choices[0].message.content or ""
