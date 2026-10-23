import os

from openai import OpenAI


def record_translate(text, target_language):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following text to {target_language}: {text}",
            }
        ],
    )
    return completion.choices[0].message.content
