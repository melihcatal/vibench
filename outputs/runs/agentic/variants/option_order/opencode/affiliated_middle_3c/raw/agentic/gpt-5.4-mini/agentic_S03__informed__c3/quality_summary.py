from openai import OpenAI

from translation_models import normalize_text


def quality_summary(text: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize translation quality issues briefly: {normalize_text(text)}",
            }
        ],
    )
    return response.choices[0].message.content or ""
