from typing import Any, Dict

import openai


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    client = openai.OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return {"provider": "openai", "model": "omni-moderation-latest", "flagged": bool(result.results[0].flagged)}
