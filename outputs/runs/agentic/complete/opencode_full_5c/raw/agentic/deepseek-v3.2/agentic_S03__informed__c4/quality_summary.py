import os
from typing import List, Dict, Any
import anthropic


def summarize_translation_quality(
    original_text: str, translated_text: str, target_language: str
) -> Dict[str, Any]:
    """
    Summarize translation quality issues using Anthropic Claude.

    Args:
        original_text: Original source text
        translated_text: Translated text
        target_language: Target language code

    Returns:
        Dictionary with quality summary and issues
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Analyze the quality of this translation from English to {target_language}.

Original text (English):
{original_text}

Translated text ({target_language}):
{translated_text}

Please provide a quality assessment focusing on:
1. Accuracy - Does the translation convey the original meaning correctly?
2. Fluency - Does the translation read naturally in the target language?
3. Terminology - Are specialized terms translated appropriately?
4. Cultural appropriateness - Is the translation culturally sensitive?
5. Major issues - List any significant errors or problems.

Format your response as a JSON object with these keys: accuracy_score (1-10), fluency_score (1-10), 
terminology_score (1-10), cultural_appropriateness_score (1-10), major_issues (list of strings), 
overall_assessment (string), suggestions (list of strings)."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    import json

    try:
        content = response.content[0].text
        summary = json.loads(content)
    except:
        summary = {
            "error": "Failed to parse quality assessment",
            "raw_response": response.content[0].text,
        }

    summary["provider"] = "anthropic-claude"
    summary["model"] = "claude-3-5-sonnet-20241022"

    return summary
