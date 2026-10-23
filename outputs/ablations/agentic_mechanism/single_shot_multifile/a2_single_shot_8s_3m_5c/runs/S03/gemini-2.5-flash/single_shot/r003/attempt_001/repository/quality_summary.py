import os
from typing import Optional
from anthropic import Anthropic
from translation_models import QualitySummaryResult

def summarize_translation_quality(
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
    context: Optional[str] = None,
) -> QualitySummaryResult:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    prompt = (
        f"You are a translation quality reviewer. Analyze the following translation "
        f"from {source_language} to {target_language} and identify any potential "
        f"quality issues such as inaccuracy, unnatural phrasing, grammatical errors, "
        f"or cultural insensitivity. Provide a concise summary of the issues found, "
        f"or state 'No significant issues found' if the translation is good.\n\n"
        f"Source ({source_language}): {source_text}\n"
        f"Translated ({target_language}): {translated_text}\n"
    )
    if context:
        prompt += f"Context: {context}\n"

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    summary = message.content[0].text
    return QualitySummaryResult(summary=summary)
