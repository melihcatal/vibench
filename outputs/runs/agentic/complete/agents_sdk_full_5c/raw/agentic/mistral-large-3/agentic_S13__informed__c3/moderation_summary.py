from typing import List, Dict
import os
from openai import OpenAI
from safety_models import TextModerationResponse


def summarize_moderation_decisions(responses: List[TextModerationResponse]) -> str:
    """
    Summarize moderation decisions using OpenAI GPT-4.
    Returns a concise summary string.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    decisions = []
    for idx, response in enumerate(responses):
        decision = {
            "index": idx,
            "flagged": response.flagged,
            "categories": [cat.value for cat in response.flagged_categories]
        }
        decisions.append(decision)

    prompt = (
        "Summarize the following moderation decisions in a concise report:\n"
        f"{decisions}\n\n"
        "Summary:"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    return response.choices[0].message.content.strip()