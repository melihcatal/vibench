from openai import OpenAI


def translate_consent_copy(text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate identity-provider consent copy into {target_language}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
