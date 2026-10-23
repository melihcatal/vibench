import os
from typing import Dict

from openai import OpenAI


MODEL = "omni-moderation-latest"


def profile_moderation(text: str) -> Dict[str, object]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model=MODEL, input=text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": item.categories.model_dump()}
