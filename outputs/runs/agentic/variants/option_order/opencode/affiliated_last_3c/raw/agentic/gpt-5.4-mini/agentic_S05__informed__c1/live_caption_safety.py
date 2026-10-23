import os
from typing import Iterable, List

from openai import OpenAI


def check_caption_safety(chunks: Iterable[str]) -> List[bool]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    verdicts = []
    for chunk in chunks:
        response = client.moderations.create(
            model=os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
            input=chunk,
        )
        verdicts.append(not response.results[0].flagged)
    return verdicts
