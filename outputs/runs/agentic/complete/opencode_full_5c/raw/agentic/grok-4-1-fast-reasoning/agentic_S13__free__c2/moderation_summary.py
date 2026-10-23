import json
from safety_client import get_openai_client
from safety_models import ModerationDecision
from typing import List


def moderation_summary(decisions: List[ModerationDecision]) -> str:
    client = get_openai_client()
    if client is None:
        raise ValueError("OpenAI API key not configured")
    decisions_json = json.dumps([dec.__dict__ for dec in decisions])
    system_prompt = "You are a moderation summary expert."
    user_prompt = f"Summarize these moderation decisions: number flagged, common categories, patterns.\\n\\n{decisions_json}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content
