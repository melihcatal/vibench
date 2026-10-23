import os
from typing import Dict, List, Optional

from openai import OpenAI


def quality_summary(
    source_texts: List[str],
    translated_texts: List[str],
    target_lang: str,
    model: str = "gpt-4o",
) -> Dict[str, List[Dict]]:
    """
    Summarizes translation quality issues using OpenAI's GPT model.

    Args:
        source_texts: List of original texts.
        translated_texts: List of translated texts.
        target_lang: The target language code (e.g., 'es').
        model: The OpenAI model to use (default: 'gpt-4o').

    Returns:
        Dictionary with keys 'issues' (list of issues per segment) and 'summary' (overall summary).

    Raises:
        ValueError: If the input lists are empty or OpenAI API call fails.
    """
    if not source_texts or not translated_texts:
        raise ValueError("Source and translated texts cannot be empty")
    if len(source_texts) != len(translated_texts):
        raise ValueError("Source and translated texts must have the same length")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    issues = []
    for src, trans in zip(source_texts, translated_texts):
        prompt = (
            f"Analyze the following translation from source text to {target_lang}. "
            f"Identify any quality issues such as mistranslations, omissions, additions, or grammatical errors. "
            f"Provide a brief summary of issues found or 'None' if no issues."
            f"\n\nSource text: {src}"
            f"\nTranslated text: {trans}"
            f"\n\nIssues:"
        )

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150,
            )
            issue_summary = response.choices[0].message.content.strip()
            issues.append(
                {
                    "source": src,
                    "translated": trans,
                    "issues": issue_summary
                    if issue_summary.lower() != "none"
                    else None,
                }
            )
        except Exception as e:
            raise ValueError(f"Failed to analyze translation quality: {e}")

    # Generate overall summary
    summary_prompt = (
        f"Provide a concise summary of the translation quality for the following segments from source to {target_lang}. "
        f"Highlight recurring issues, overall accuracy, and fluency.\n\n"
        f"Segments analyzed: {len(source_texts)}"
    )

    try:
        summary_response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        overall_summary = summary_response.choices[0].message.content.strip()
    except Exception as e:
        raise ValueError(f"Failed to generate quality summary: {e}")

    return {
        "issues": issues,
        "summary": overall_summary,
    }
