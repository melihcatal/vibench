from __future__ import annotations

from typing import List

from safety_client import get_client, get_config


def moderation_summary(decisions: List[str]) -> str:
    config = get_config()
    client = get_client(config.api_key)
    prompt = "Summarize the following moderation decisions for an ops reviewer:\n" + "\n".join(decisions)
    response = client.responses.create(
        model=config.chat_model,
        input=prompt,
    )
    return response.output_text
