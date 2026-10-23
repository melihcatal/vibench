# [LATER-STEP] quality_summary.py

# Summarizes translation quality issues.
# Uses OpenAI Chat Completion as a hosted LLM inference service.
import os
import json
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

client = OpenAI(api_key=openai_api_key)


def summarize_quality(translated_texts: list[str], original_texts: list[str]) -> str:
    """Generate a concise summary of translation quality issues.","""
    if len(translated_texts) != len(original_texts):
        raise ValueError("translated_texts and original_texts must have equal length")
    messages = [
        {
            "role": "system",
            "content": "You are a QA analyst. Given original text and its translation, list any quality issues (grammar, meaning drift, missing words, etc.) in a concise markdown bullet list. Be brief.",
        }
    ]
    for orig, trans in zip(original_texts, translated_texts):
        messages.append(
            {"role": "user", "content": f"Original: {orig}\nTranslation: {trans}"}
        )
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, max_tokens=500
    )
    return response.choices[0].message.content.strip()
