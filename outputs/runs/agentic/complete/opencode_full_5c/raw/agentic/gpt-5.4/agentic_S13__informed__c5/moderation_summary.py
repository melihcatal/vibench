from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

from safety_models import ModerationResult, result_to_dict


def moderation_summary(results: List[ModerationResult]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    payload: List[Dict[str, Any]] = [result_to_dict(item) for item in results]
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize moderation outcomes for internal trust and safety reviewers.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": str(payload)}],
            },
        ],
    )
    return response.output_text
