import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_quality_summary(
    original_text: str, translated_text: str, source_lang: str, target_lang: str
) -> str:
    prompt = f"""
Analyze the following translation from {source_lang} to {target_lang}:

Original: {original_text}

Translated: {translated_text}

Provide a concise summary of any quality issues (e.g., accuracy, fluency, omissions) or confirm high quality.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
