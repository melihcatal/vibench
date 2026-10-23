import os
from typing import List

import cohere


def script_embedding(text: str) -> List[float]:
    client = cohere.Client(os.environ["COHERE_API_KEY"])
    response = client.embed(texts=[text], model="embed-english-v3.0")
    return list(response.embeddings[0])
