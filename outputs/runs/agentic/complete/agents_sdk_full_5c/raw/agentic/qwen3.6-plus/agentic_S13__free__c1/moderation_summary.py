"""
[LATER-STEP] moderation_summary.py
Summarize moderation decisions.
Uses the OpenAI Chat Completions API (openai SDK, gpt-4o model).
"""

import json
from typing import Optional

from openai import OpenAI

from safety_client import get_openai_client
from safety_models import ModerationResponse, BatchModerationResponse


OPENAI_CHAT_MODEL = "gpt-4o"


def summarize_single_decision(
    text: str,
    response: ModerationResponse,
    api_key: Optional[str] = None,
    model: str = OPENAI_CHAT_MODEL,
) -> str:
    """
    Generate a human-readable summary of a single moderation decision.

    Args:
        text: The original text that was moderated.
        response: ModerationResponse from the OpenAI Moderation API.
        api_key: Optional OpenAI API key.
        model: OpenAI chat model identifier (default: gpt-4o).

    Returns:
        A concise summary string describing the moderation decision.
    """
    client = get_openai_client(api_key=api_key)

    flagged_cats = [
        c for c in response.categories if c.flagged or c.score > 0.3
    ]
    cat_summary = ", ".join(
        f"{c.category} (score: {c.score:.3f})" for c in flagged_cats
    ) or "none"

    system_prompt = (
        "You are a content moderation analyst. Provide a brief, professional "
        "summary of the moderation decision for the given text."
    )
    user_prompt = (
        f"Text (truncated to 500 chars): {text[:500]}\n\n"
        f"Moderation result: flagged={response.flagged}\n"
        f"Flagged categories: {cat_summary}\n\n"
        f"Summarize the decision in 2-3 sentences."
    )

    chat_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=150,
        temperature=0.3,
    )

    return chat_response.choices[0].message.content.strip()


def summarize_batch_decisions(
    texts: list[str],
    batch_response: BatchModerationResponse,
    api_key: Optional[str] = None,
    model: str = OPENAI_CHAT_MODEL,
) -> str:
    """
    Generate a summary of moderation decisions across a batch of texts.

    Args:
        texts: The original list of texts.
        batch_response: BatchModerationResponse from moderate_batch.
        api_key: Optional OpenAI API key.
        model: OpenAI chat model identifier (default: gpt-4o).

    Returns:
        A summary string describing the batch moderation outcomes.
    """
    client = get_openai_client(api_key=api_key)

    total = len(texts)
    flagged_count = len(batch_response.all_flagged)
    safe_count = batch_response.safe_count

    top_categories: dict[str, int] = {}
    for result in batch_response.results:
        for cat in result.categories:
            if cat.flagged:
                top_categories[cat.category] = top_categories.get(cat.category, 0) + 1

    stats = (
        f"Total messages: {total}\n"
        f"Flagged: {flagged_count}\n"
        f"Safe: {safe_count}\n"
        f"Top flagged categories: {json.dumps(top_categories)}"
    )

    system_prompt = (
        "You are a content moderation analyst. Provide a concise executive summary "
        "of moderation results for a batch of user messages."
    )
    user_prompt = (
        f"Batch moderation statistics:\n{stats}\n\n"
        f"Provide a 3-4 sentence summary of the batch outcomes and any patterns."
    )

    chat_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=200,
        temperature=0.3,
    )

    return chat_response.choices[0].message.content.strip()
