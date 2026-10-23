from typing import Dict, List
from safety_models import ModerationSummary, BatchModerationResult
from openai import OpenAI
import os


def summarize_moderation_decisions(
    batch_result: BatchModerationResult,
) -> ModerationSummary:
    """Summarize moderation decisions using OpenAI GPT."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    flagged_messages = sum(1 for result in batch_result.results if not result.is_safe)
    flagged_categories = {}

    for result in batch_result.results:
        if not result.is_safe:
            for category, score in result.categories.items():
                if score >= 0.75:
                    flagged_categories[category] = (
                        flagged_categories.get(category, 0) + 1
                    )

    safety_score = (
        1.0 - (flagged_messages / len(batch_result.results))
        if batch_result.results
        else 1.0
    )

    summary_prompt = (
        f"Summarize the following moderation results:\n"
        f"Total messages: {len(batch_result.results)}\n"
        f"Flagged messages: {flagged_messages}\n"
        f"Flagged categories: {flagged_categories}\n"
        f"Safety score: {safety_score:.2f}\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a moderation summary assistant."},
            {"role": "user", "content": summary_prompt},
        ],
    )

    summary_text = response.choices[0].message.content.strip()

    return ModerationSummary(
        total_messages=len(batch_result.results),
        flagged_messages=flagged_messages,
        flagged_categories=flagged_categories,
        safety_score=safety_score,
    )
