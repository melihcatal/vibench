import os
from openai import OpenAI


def record_translate(text, target_language):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following text to {target_language}: {text}",
            }
        ],
    )
    return response.choices[0].message.content
