import os
from openai import OpenAI


def summarize_translation_quality(
    original: str, translated: str, source_lang: str = "EN", target_lang: str = "FR"
) -> str:
    """
    Summarizes translation quality issues using OpenAI GPT-4o-mini.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Analyze the translation from {source_lang} "{original}" to {target_lang} "{translated}".

Summarize quality issues: accuracy, fluency, omissions, awkward phrasing, etc.
If excellent, state that. Keep under 200 words."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()
