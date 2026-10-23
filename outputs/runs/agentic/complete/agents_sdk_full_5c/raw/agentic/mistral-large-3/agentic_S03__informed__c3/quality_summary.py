from typing import List, Dict, Any
import os
from openai import OpenAI
from translation_models import BatchTranslationResponse

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def quality_summary(source_texts: List[str], translated_texts: List[str], target_lang: str) -> Dict[str, Any]:
    prompt = (
        f"You are a translation quality reviewer. Given the following source texts and their translations to {target_lang}, "
        "provide a summary of potential quality issues, including fluency, accuracy, and cultural appropriateness. "
        "Source texts: \n"
        f"{source_texts}\n\n"
        "Translated texts: \n"
        f"{translated_texts}\n\n"
        "Provide a structured summary of issues:"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response.choices[0].message.content
    return {"quality_summary": summary}