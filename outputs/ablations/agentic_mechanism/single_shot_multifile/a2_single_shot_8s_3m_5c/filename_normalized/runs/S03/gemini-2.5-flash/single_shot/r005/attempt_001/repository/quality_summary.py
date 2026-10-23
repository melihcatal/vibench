import os
from typing import Dict, Any
from translation_client import get_openai_client

def summarize_translation_quality(
    original_text: str,
    translated_text: str,
    source_language: str,
    target_language: str
) -> Dict[str, Any]:
    client = get_openai_client()

    prompt = (
        f"Analyze the translation quality from {source_language} to {target_language}. "
        f"Original: '{original_text}'. Translated: '{translated_text}'. "
        "Provide a brief summary of any potential issues like accuracy, fluency, or style. "
        "Suggest a quality score out of 5 based on your assessment."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that assesses translation quality."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    summary = response.choices[0].message.content
    try:
        score_phrase = "quality score out of 5:"
        if score_phrase in summary.lower():
            start_index = summary.lower().find(score_phrase) + len(score_phrase)
            score_str = summary[start_index:].strip().split(' ')[0]
            score = float(score_str)
        else:
            score = None
    except (ValueError, IndexError):
        score = None

    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "summary": summary,
        "quality_score": score
    }
