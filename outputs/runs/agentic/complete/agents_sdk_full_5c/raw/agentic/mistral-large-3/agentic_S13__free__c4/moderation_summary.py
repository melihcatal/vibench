"""
Summarize moderation decisions using OpenAI's GPT-4 model.
"""
import os
from typing import List, Dict
import openai
from safety_models import TextModerationResult


def generate_moderation_summary(results: List[TextModerationResult]) -> str:
    """Generate a summary of moderation decisions using OpenAI's GPT-4."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")

    decisions = []
    for result in results:
        decision = {
            "text": result.text,
            "scores": {score.category: score.score for score in result.scores}
        }
        decisions.append(decision)

    prompt = (
        "Summarize the following moderation decisions in a concise report. "
        "Highlight trends, high-risk categories, and overall compliance:\n\n"
        f"{decisions}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response.choices[0].message.content.strip()