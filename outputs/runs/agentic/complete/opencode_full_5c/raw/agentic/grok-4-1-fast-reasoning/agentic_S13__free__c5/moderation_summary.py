import os
import json
from typing import List
from openai import OpenAI
from safety_models import ModerationResult


def moderation_summary(results: List[ModerationResult]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Provide a concise summary of these content moderation decisions, highlighting patterns, statistics, and recommendations:\\n"
        + json.dumps(results, indent=2)
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at summarizing content moderation logs.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()
