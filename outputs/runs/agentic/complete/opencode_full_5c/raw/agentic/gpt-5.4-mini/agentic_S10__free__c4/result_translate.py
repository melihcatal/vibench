from openai import OpenAI


def result_translate(text: str, target_language: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the text into {target_language}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return completion.choices[0].message.content
