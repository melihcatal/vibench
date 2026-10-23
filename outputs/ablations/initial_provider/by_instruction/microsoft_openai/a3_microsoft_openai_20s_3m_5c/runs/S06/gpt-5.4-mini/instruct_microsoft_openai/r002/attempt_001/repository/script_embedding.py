from typing import List

from speech_client import client, default_embedding_model


def embed_script(text: str) -> List[float]:
    response = client().embeddings.create(model=default_embedding_model(), input=text)
    return response.data[0].embedding
