import os
from typing import Dict, List, Optional

from openai import OpenAI


def unsafe_copy_check(
    texts: List[str],
    language: str,
    model: str = "gpt-4o",
) -> Dict[str, Dict]:
    """
    Checks localized copy for unsafe content using OpenAI's GPT model.

    Args:
        texts: List of texts to check for unsafe content.
        language: The language of the texts (e.g., 'es').
        model: The OpenAI model to use (default: 'gpt-4o').

    Returns:
        Dictionary with keys as input texts and values as dictionaries containing:
        - 'is_unsafe': Boolean indicating if content is unsafe.
        - 'issues': List of issues found (empty if safe).

    Raises:
        ValueError: If the input list is empty or OpenAI API call fails.
    """
    if not texts:
        raise ValueError("Texts cannot be empty")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    results = {}
    for text in texts:
        prompt = (
            f"Analyze the following text in {language} for unsafe, harmful, or inappropriate content. "
            f"Check for hate speech, violence, self-harm, sexual content, profanity, or other harmful material. "
            f"Provide a list of issues found or 'None' if no issues.\n\n"
            f"Text: {text}\n\n"
            f"Issues:"
        )

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150,
            )
            issues = response.choices[0].message.content.strip()
            results[text] = {
                "is_unsafe": issues.lower() != "none",
                "issues": issues if issues.lower() != "none" else [],
            }
        except Exception as e:
            raise ValueError(f"Failed to check for unsafe content: {e}")

    return results
