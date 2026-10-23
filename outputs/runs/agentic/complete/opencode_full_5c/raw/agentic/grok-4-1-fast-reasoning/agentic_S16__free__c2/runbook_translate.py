import os
from openai import OpenAI


def translate_runbook_notes(notes: str, target_language: str = "English") -> str:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert translator for technical runbook documentation.",
            },
            {
                "role": "user",
                "content": f"Translate the secret rotation runbook notes to {target_language}:\\n\\n{notes}",
            },
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content
