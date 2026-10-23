from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptChunk, normalize_text


def translate_live_captions(chunks: Iterable[TranscriptChunk], target_language: str = "es") -> List[str]:
    client = OpenAI()
    texts = [normalize_text(chunk.text) for chunk in chunks if chunk.text]
    if not texts:
        return []
    prompt = "\n".join(texts)
    response = client.responses.create(model="gpt-4o-mini", input=f"Translate to {target_language}: {prompt}")
    return [response.output_text]
