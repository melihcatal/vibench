from typing import Any, Dict

import openai


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = openai.OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"provider": "openai", "flagged": result.flagged, "categories": result.categories}
