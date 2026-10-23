import os
from anthropic import Anthropic
from typing import List, Dict, Any


def summarize_translation_quality(
    original_text: str, translated_text: str, source_language: str, target_language: str
) -> Dict[str, Any]:
    """Summarize translation quality issues using Anthropic Claude."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Analyze the quality of this translation and identify any issues:

Source language: {source_language}
Target language: {target_language}

Original text: {original_text}

Translated text: {translated_text}

Please provide a quality assessment with the following:
1. Overall quality score (1-10)
2. Accuracy of meaning preservation
3. Grammatical correctness
4. Naturalness/fluency in target language
5. Cultural appropriateness
6. Specific issues found (if any)
7. Suggestions for improvement (if needed)

Format your response as a structured analysis."""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language,
        "quality_analysis": response.content[0].text,
        "model_used": "claude-3-sonnet-20240229",
    }
