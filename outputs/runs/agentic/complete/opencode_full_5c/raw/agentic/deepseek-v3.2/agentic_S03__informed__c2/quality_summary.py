import openai
import os
from typing import Dict, List, Any


def summarize_translation_quality(
    source_text: str, translated_text: str, target_language: str
) -> Dict[str, Any]:
    """
    Summarize translation quality issues using GPT via OpenAI.

    Args:
        source_text: Original source text
        translated_text: Translated text
        target_language: Target language code

    Returns:
        Dictionary with quality summary and issues
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Analyze the quality of this translation from the source language to {target_language}.
    
    Source text: {source_text}
    
    Translated text: {translated_text}
    
    Please provide a quality assessment including:
    1. Accuracy of translation
    2. Grammar and syntax issues
    3. Cultural appropriateness
    4. Naturalness of language
    5. Any mistranslations or omissions
    6. Overall quality score (1-10)
    
    Format your response as a structured analysis.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translation quality analyst.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    analysis_text = response.choices[0].message.content

    return {
        "source_text": source_text,
        "translated_text": translated_text,
        "target_language": target_language,
        "quality_analysis": analysis_text,
        "model_used": "gpt-4",
        "provider": "OpenAI",
    }
