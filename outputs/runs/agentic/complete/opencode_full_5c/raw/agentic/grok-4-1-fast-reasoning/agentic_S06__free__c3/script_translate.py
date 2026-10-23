import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate_script(script: str, target_language: str = "es") -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the narration script to {target_language} accurately and fluently, preserving meaning and tone.",
            },
            {"role": "user", "content": script},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
