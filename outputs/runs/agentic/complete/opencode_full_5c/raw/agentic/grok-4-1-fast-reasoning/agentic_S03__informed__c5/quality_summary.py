import openai
import os
from typing import Optional


def summarize_translation_quality(
    original_text: str, translated_text: str, model: str = "gpt-4o-mini"
) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""You are a translation quality expert. Analyze the following translation:

Original: {original_text}

Translated: {translated_text}

Provide a concise summary of quality issues (accuracy, fluency, naturalness, omissions, etc.). If high quality, note it. Use bullet points."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, precise translation quality assessor.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
