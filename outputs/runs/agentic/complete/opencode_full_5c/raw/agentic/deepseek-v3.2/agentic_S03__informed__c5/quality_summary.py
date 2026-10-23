import os
from typing import Dict, List, Optional
import json


def quality_summary(
    original_text: str, translated_text: str, target_language: str
) -> Dict[str, any]:
    """
    Summarize translation quality issues using an LLM.

    Args:
        original_text: Original source text
        translated_text: Translated text
        target_language: Target language code

    Returns:
        Dictionary with quality assessment and issues
    """
    # Use OpenAI GPT-4 for quality assessment
    import openai

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
    Analyze the quality of this translation from English to {target_language}.
    
    Original text (English):
    {original_text}
    
    Translated text ({target_language}):
    {translated_text}
    
    Please provide a quality assessment with the following:
    1. Overall quality score (0-100)
    2. Accuracy assessment (how well it conveys the original meaning)
    3. Fluency assessment (how natural it sounds in the target language)
    4. Cultural appropriateness
    5. List of specific issues found (if any)
    6. Suggestions for improvement (if needed)
    
    Return your assessment as a JSON object with these fields:
    - overall_score: integer 0-100
    - accuracy: string assessment
    - fluency: string assessment  
    - cultural_appropriateness: string assessment
    - issues: list of strings
    - suggestions: list of strings
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translation quality analyst. Provide detailed, objective assessments of translation quality.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    # Parse the JSON response
    result_text = response.choices[0].message.content
    assessment = json.loads(result_text)

    # Add metadata
    assessment["provider"] = "openai"
    assessment["model"] = "gpt-4"
    assessment["target_language"] = target_language

    return assessment
