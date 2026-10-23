from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptChunk, normalize_text


def check_live_caption_safety(chunks: Iterable[TranscriptChunk]) -> List[str]:
    client = OpenAI()
    text = "\n".join(normalize_text(chunk.text) for chunk in chunks if chunk.text)
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return [str(result.flagged) for result in response.results]
