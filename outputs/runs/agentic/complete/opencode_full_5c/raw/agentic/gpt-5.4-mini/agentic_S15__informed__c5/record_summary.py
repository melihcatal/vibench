from openai import OpenAI


def record_summary(text: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize document records concisely."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
