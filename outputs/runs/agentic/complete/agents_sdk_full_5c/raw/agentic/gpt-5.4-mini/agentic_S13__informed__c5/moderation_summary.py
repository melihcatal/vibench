from openai import OpenAI


def moderation_summary(decisions: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize moderation decisions concisely."},
            {"role": "user", "content": decisions},
        ],
    )
    return response.choices[0].message.content or ""
