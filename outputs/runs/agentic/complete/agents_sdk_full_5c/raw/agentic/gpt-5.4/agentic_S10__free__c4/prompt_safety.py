from __future__ import annotations

from typing import Dict

from openai import OpenAI

from model_client import DEFAULT_MODERATION_MODEL
from model_models import ModerationResult


def check_prompt_safety(prompt: str, generated_text: str = "") -> Dict[str, ModerationResult]:
    client = OpenAI()
    prompt_response = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=prompt,
    )
    output_response = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=generated_text,
    )

    prompt_result = prompt_response.results[0]
    output_result = output_response.results[0]

    return {
        "prompt": ModerationResult(
            flagged=prompt_result.flagged,
            categories=prompt_result.categories.model_dump(),
            model=prompt_response.model,
            raw=prompt_response,
        ),
        "generated_text": ModerationResult(
            flagged=output_result.flagged,
            categories=output_result.categories.model_dump(),
            model=output_response.model,
            raw=output_response,
        ),
    }
