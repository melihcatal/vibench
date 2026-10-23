import os

from openai import OpenAI


def generate_spoken_brief(results: list[str]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini"),
        messages=[
            {
                "role": "user",
                "content": "Summarize these search results: " + " | ".join(results),
            }
        ],
    )
    return completion.choices[0].message.content or ""
