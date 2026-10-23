from typing import Mapping

from openai import OpenAI


def claims_moderation(claims: Mapping[str, object]) -> dict[str, object]:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=str(dict(claims)))
    result = response.results[0] if response.results else None
    flagged = bool(getattr(result, "flagged", False))
    return {"provider": "openai", "model": "omni-moderation-latest", "flagged": flagged}
