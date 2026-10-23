from openai import OpenAI
from typing import List, Dict, Any
import os

# Provider: OpenAI GPT
# Model: gpt-4o-mini


def quality_summary(translations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarizes translation quality issues using OpenAI GPT.

    Args:
        translations: A list of dictionaries containing 'source', 'target', and 'translated_text'.

    Returns:
        A summary of translation quality issues.
    """
    if not translations:
        return {"summary": "No translations provided."}

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        "Analyze the following translations for quality issues such as fluency, accuracy, and cultural appropriateness. "
        "Provide a summary of any issues found:\n\n"
    )

    for item in translations:
        prompt += (
            f"Source ({item.get('source_language', 'unknown')}): {item.get('source', '')}\n"
            f"Target ({item.get('target_language', 'unknown')}): {item.get('translated_text', '')}\n\n"
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a translation quality analyst."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
    )

    return {"summary": response.choices[0].message.content.strip()}
