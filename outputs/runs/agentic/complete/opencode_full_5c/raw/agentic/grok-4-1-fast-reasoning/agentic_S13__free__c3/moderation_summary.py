import anthropic
from typing import List
from safety_client import get_api_key
from safety_models import ModerationResult


def moderation_summary(results: List[ModerationResult]) -> str:
    client = anthropic.Anthropic(api_key=get_api_key("anthropic"))
    summary_input = "\\n".join(
        [
            f"Text: {r.input_text[:100]}... | Flagged: {r.flagged} | Scores: {[(s.category, round(s.probability, 3)) for s in r.scores]}"
            for r in results
        ]
    )
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the moderation decisions from these results in a concise report:\\n{summary_input}",
            }
        ],
    )
    return message.content[0].text
