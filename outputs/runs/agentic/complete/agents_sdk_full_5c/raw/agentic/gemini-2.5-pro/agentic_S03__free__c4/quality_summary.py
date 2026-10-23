import os
import cohere

from translation_client import get_cohere_api_key
from translation_models import QualitySummary

def summarize_quality_issues(original_text: str, translated_text: str) -> QualitySummary:
    """
    Uses Cohere to summarize potential quality issues in a translation.

    Args:
        original_text: The source text.
        translated_text: The translated text.

    Returns:
        A QualitySummary object with a summary of issues.
    """
    api_key = get_cohere_api_key()
    co = cohere.Client(api_key)

    prompt = f"""
    Analyze the following English source text and its translation to identify potential quality issues.
    Issues could include loss of nuance, grammatical errors, awkward phrasing, or mistranslations.
    Provide a brief summary of the overall quality.

    Source Text:
    "{original_text}"

    Translated Text:
    "{translated_text}"

    Summary of potential issues:
    """

    response = co.chat(
        model="command-r",
        message=prompt,
        temperature=0.3,
    )

    summary_text = response.text

    # This is a placeholder for a more sophisticated scoring logic
    score = 1.0 - (summary_text.lower().count("issue") * 0.1)
    issues = [
        line.strip() for line in summary_text.split("\n") if line.strip()
    ]

    return QualitySummary(
        score=max(0.0, score),
        issues=issues,
        summary_text=summary_text,
    )
