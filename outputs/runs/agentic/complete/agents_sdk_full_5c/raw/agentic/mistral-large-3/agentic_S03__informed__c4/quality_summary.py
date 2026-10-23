import os
from openai import OpenAI
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_translation_quality(source_texts: List[str], translated_texts: List[str], target_language: str) -> str:
    prompt = (
        f"Analyze the following translations from a source language to {target_language}. "
        f"Provide a summary of translation quality, noting any inaccuracies, omissions, or stylistic issues:\n\n"
        f"Source Texts: {source_texts}\n\n"
        f"Translated Texts: {translated_texts}\n\n"
        f"Summary:"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()