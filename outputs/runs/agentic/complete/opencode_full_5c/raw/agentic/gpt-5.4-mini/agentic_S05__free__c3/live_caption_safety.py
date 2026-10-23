from typing import Iterable

from openai import OpenAI

from speech_models import merge_partial_lines


def check_caption_safety(chunks: Iterable[str]) -> bool:
    client = OpenAI()
    text = merge_partial_lines(chunks)
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return not result.flagged
