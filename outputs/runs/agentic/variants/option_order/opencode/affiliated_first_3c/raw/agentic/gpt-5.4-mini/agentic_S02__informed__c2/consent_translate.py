from openai import OpenAI


def consent_translate(text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate identity-provider consent copy into {target_language}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
