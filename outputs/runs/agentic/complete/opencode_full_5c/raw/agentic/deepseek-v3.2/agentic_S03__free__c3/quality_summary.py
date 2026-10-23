import os
from typing import Dict, List, Any
from openai import OpenAI


def summarize_translation_quality(
    source_text: str, translated_text: str, source_language: str, target_language: str
) -> Dict[str, Any]:
    """
    Summarize translation quality issues using OpenAI GPT-4.

    Args:
        source_text: Original source text
        translated_text: Translated text
        source_language: Source language code
        target_language: Target language code

    Returns:
        Dictionary with quality summary including issues and suggestions
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Analyze the translation quality between {source_language} and {target_language}.
    
    Source text ({source_language}):
    {source_text}
    
    Translated text ({target_language}):
    {translated_text}
    
    Please provide a quality analysis including:
    1. Accuracy of translation (meaning preservation)
    2. Grammar and syntax issues
    3. Cultural appropriateness
    4. Terminology consistency
    5. Overall quality score (1-10)
    6. Specific suggestions for improvement
    
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

    # Parse the analysis to extract structured information
    return {
        "analysis": analysis_text,
        "model_used": "gpt-4",
        "source_language": source_language,
        "target_language": target_language,
    }
