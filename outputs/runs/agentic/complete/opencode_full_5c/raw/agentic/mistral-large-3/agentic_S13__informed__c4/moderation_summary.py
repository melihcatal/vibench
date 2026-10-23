from typing import Dict, List
from openai import OpenAI
import os


def summarize_moderation_decisions(decisions: List[Dict]) -> str:
    """Summarize moderation decisions using OpenAI GPT-4."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        "Summarize the following moderation decisions in a concise report:\n"
        f"{decisions}\n\n"
        "Include the total number of flagged messages, the most common categories, "
        "and any notable patterns."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()
