from cohere import Client
import os
from typing import List

def embed_output(text: str) -> List[float]:
    client = Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings[0]