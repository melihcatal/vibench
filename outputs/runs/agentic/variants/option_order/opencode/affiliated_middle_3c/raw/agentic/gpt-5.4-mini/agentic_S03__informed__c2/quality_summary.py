import os

from openai import OpenAI


def quality_summary(translation_text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize translation quality issues concisely.",
            },
            {"role": "user", "content": translation_text},
        ],
    )
    return resp.choices[0].message.content or ""
