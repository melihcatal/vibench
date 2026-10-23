from typing import List

import cohere


def embed_messages(messages: List[str]) -> List[List[float]]:
    client = cohere.Client(api_key=None)
    response = client.embed(
        texts=messages, model="embed-english-v3.0", input_type="search_document"
    )
    return list(response.embeddings)
