from typing import Dict
from moderation import ModerationClient


def profile_moderation(text: str) -> Dict[str, str]:
    client = ModerationClient()

    response = client.moderate(text=text, models=["text-moderation-stable"])

    return {
        "flagged": str(response["results"][0]["flagged"]).lower(),
        "categories": str(response["results"][0]["categories"]),
        "score": str(response["results"][0]["score"]),
    }
