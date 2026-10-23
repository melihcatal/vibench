import openai
import os
from typing import List

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_quality_summary(
    original_texts: List[str],
    translated_texts: List[str],
    source_lang: str,
    target_lang: str
) -> str:
    prompt = f"""Summarize translation quality issues from {source_lang} to {target_lang}.

Original: {'; '.join(original_texts)}
Translated: {'; '.join(translated_texts)}

Be concise, list key issues or say "No significant issues.""""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()