from openai import OpenAI


def appeal_translate(appeal_text: str, target_language: str = "en") -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": f"Translate appeal text into {target_language} for review."},
            {"role": "user", "content": appeal_text},
        ],
    )
    return response.choices[0].message.content or ""
