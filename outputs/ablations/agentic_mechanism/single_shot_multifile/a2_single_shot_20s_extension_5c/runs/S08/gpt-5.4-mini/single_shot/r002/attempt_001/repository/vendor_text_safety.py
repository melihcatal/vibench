import os
from typing import Dict

from openai import OpenAI

SAFETY_MODEL_ID = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def vendor_text_safety(text: str) -> Dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.moderations.create(model=SAFETY_MODEL_ID, input=text)
    category_scores = result.results[0].category_scores.model_dump() if result.results else {}
    flagged = result.results[0].flagged if result.results else False
    return {"provider": "openai", "model": SAFETY_MODEL_ID, "flagged": flagged, "category_scores": category_scores}
