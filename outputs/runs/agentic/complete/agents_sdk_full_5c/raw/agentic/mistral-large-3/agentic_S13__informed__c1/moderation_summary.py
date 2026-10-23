import os
from typing import Dict, Any, List
from openai import OpenAI


def generate_moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    """Generate a summary of moderation decisions using OpenAI GPT-4."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key must be set.")

    client = OpenAI(api_key=api_key)

    prompt = (
        "Summarize the following moderation decisions in a concise report. "
        "Include the number of allowed and blocked messages, and the most common reasons for blocking.\n\n"
        f"Decisions: {decisions}"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()