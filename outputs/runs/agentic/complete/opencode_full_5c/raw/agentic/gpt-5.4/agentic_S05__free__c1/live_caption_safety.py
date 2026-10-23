from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


def check_live_caption_safety(captions: Iterable[str]) -> List[dict]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    results: List[dict] = []
    for caption in captions:
        moderation = client.moderations.create(
            model="omni-moderation-latest", input=caption
        )
        results.append(moderation.results[0].model_dump())
    return results
