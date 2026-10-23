from typing import Any, Dict

from openai import OpenAI


def profile_moderation(profile_text: str) -> Dict[str, Any]:
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=profile_text)
    flagged = result.results[0].flagged if result.results else False
    return {"flagged": flagged, "categories": result.results[0].categories if result.results else {}}


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    event = event or {}
    return profile_moderation(event["profile_text"])
