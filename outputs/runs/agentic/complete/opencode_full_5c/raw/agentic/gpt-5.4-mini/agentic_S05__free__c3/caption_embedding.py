from typing import Iterable, List

from openai import OpenAI

from speech_models import merge_partial_lines


def embed_caption_chunks(chunks: Iterable[str]) -> List[float]:
    client = OpenAI()
    text = merge_partial_lines(chunks)
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return list(response.data[0].embedding)
