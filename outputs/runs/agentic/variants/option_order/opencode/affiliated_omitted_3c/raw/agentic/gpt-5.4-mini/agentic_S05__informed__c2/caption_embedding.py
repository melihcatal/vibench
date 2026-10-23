from typing import Iterable, List

from cohere import ClientV2


def embed_captions(captions: Iterable[str]) -> List[List[float]]:
    client = ClientV2()
    response = client.embed(
        model="embed-english-v3.0", texts=list(captions), input_type="search_document"
    )
    return [list(vector) for vector in response.embeddings]
