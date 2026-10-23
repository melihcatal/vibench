import os

from openai import OpenAI


def appeal_translate(text, target_language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate this appeal into {target_language}: {text}",
            }
        ],
    )
    return response.choices[0].message.content
