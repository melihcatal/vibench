import os

import openai


def compliance_note_translate(text, target_language):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate this compliance note to {target_language}: {text}",
            }
        ],
    )
    return response.choices[0].message.content
