from openai import OpenAI


def rotation_summary(notes: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": notes}]
    )
    return response.choices[0].message.content
