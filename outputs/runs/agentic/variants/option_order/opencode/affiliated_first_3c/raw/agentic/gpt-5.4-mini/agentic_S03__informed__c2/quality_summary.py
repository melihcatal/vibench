import os

from openai import OpenAI


def quality_summary(text: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize translation quality issues succinctly.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
