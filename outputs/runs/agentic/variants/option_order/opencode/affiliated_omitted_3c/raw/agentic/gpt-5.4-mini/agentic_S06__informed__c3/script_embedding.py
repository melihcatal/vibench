from typing import List

import cohere


def embed_script(texts: List[str]) -> List[List[float]]:
    client = cohere.Client()
    resp = client.embed(texts=texts, model="embed-english-v3.0", input_type="search_document")
    return resp.embeddings
