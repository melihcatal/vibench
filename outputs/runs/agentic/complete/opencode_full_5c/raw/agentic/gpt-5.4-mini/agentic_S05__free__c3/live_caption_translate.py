from typing import Iterable, List

from openai import OpenAI

from speech_models import merge_partial_lines


def translate_captions(chunks: Iterable[str], target_language: str = "es") -> str:
    client = OpenAI()
    text = merge_partial_lines(chunks)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following live captions into {target_language}: {text}",
    )
    return response.output_text
