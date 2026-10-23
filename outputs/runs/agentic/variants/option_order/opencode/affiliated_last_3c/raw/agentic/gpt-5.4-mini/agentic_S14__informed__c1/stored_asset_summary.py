from openai import OpenAI


def summarize_asset(text: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize the asset concisely."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
