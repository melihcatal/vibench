from __future__ import annotations

from typing import Any

from openai import OpenAI

from safety_client import openai_config


def moderation_summary(decisions: list[dict[str, Any]]) -> str:
    config = openai_config()
    client = OpenAI(api_key=config["api_key"])
    prompt = {
        "role": "user",
        "content": f"Summarize these moderation decisions for an internal reviewer in 3 concise bullet points: {decisions}",
    }
    response = client.responses.create(model=config["model"], input=[prompt])
    return response.output_text
