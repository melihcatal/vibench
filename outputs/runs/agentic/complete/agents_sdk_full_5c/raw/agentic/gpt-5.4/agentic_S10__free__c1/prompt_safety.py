from __future__ import annotations

from typing import Dict

from model_client import DEFAULT_MODERATION_MODEL, get_openai_client
from model_models import SafetyCheckResult


def check_prompt_safety(prompt: str, generated_text: str) -> Dict[str, SafetyCheckResult]:
    client = get_openai_client()
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
        "prompt": SafetyCheckResult(
            flagged=prompt_result.flagged,
            categories=prompt_result.categories.model_dump(),
            raw_response=prompt_response.model_dump(),
        ),
        "generated_text": SafetyCheckResult(
            flagged=output_result.flagged,
            categories=output_result.categories.model_dump(),
            raw_response=output_response.model_dump(),
        ),
    }
