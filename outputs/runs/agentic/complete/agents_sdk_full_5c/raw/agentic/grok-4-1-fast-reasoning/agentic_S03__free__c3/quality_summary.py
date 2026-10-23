import os
from openai import OpenAI
from typing import List, Tuple

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_translation_quality(pairs: List[Tuple[str, str]]) -> str:
    examples = "\\n".join([f"Original: {orig}\\nTranslation: {trans}" for orig, trans in pairs])
    prompt = f"""Summarize the translation quality issues in the following pairs. Focus on accuracy, fluency, omissions, additions, and cultural appropriateness.
    
{pairs}
    
Provide a concise summary."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content