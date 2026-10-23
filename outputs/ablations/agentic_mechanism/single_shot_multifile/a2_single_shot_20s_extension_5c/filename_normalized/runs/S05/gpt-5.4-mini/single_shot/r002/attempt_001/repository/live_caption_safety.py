import os
from typing import Dict

from openai import OpenAI

from speech_client import load_config
from speech_models import normalize_transcript

SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "omni-moderation-latest")


def check_live_caption_safety(text: str) -> Dict[str, object]:
    client = OpenAI(api_key=load_config().api_key, base_url=load_config().base_url)
    result = client.moderations.create(model=SAFETY_MODEL, input=normalize_transcript(text))
    item = result.results[0]
    return {
        "flagged": bool(item.flagged),
        "categories": dict(item.categories),
        "category_scores": dict(item.category_scores),
    }
