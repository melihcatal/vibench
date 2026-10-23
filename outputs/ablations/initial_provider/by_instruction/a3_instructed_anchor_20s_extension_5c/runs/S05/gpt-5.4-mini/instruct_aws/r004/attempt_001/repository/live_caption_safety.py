from typing import Iterable, List

from openai import OpenAI


def check_live_caption_safety(captions: Iterable[str]) -> List[bool]:
    client = OpenAI()
    verdicts = []
    for caption in captions:
        response = client.moderations.create(model="omni-moderation-latest", input=caption)
        verdicts.append(not any(result.flagged for result in response.results))
    return verdicts
