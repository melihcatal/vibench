from openai import OpenAI


def spoken_brief(text: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Rewrite the text as a brief spoken update."},
            {"role": "user", "content": text},
        ],
    )
    return completion.choices[0].message.content
