import os
from anthropic import Anthropic
from typing import Optional


def summarize_quality_issues(
    translated_text: str, original_text: str, source_lang: str, target_lang: str
) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    prompt = f"""Given the original text in {source_lang} and its translation in {target_lang}, identify and summarize any potential quality issues such as grammatical errors, unnatural phrasing, mistranslations, or cultural insensitivity.

Original ({source_lang}):
{original_text}

Translated ({target_lang}):
{translated_text}

Summary of quality issues:"""

    message = client.messages.create(
        model="claude-3-opus-20240229",  # Using a concrete model identifier
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
