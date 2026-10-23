import os
from openai import OpenAI
from typing import Optional

def summarize_translation_quality(
    source_text: str, translated_text: str, target_lang: Optional[str] = None
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {
            "role": "system",
            "content": (
                "You are a translation quality expert. Summarize any quality issues such as "
                "inaccuracies, unnatural phrasing, omissions, or cultural mismatches. "
                "Be concise. If no issues, say 'High quality translation.'"
            ),
        },
        {
            "role": "user",
            "content": f"Source: {source_text}\\nTarget ({target_lang}): {translated_text}",
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=150,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
