import os
from typing import List

from cohere import ClientV2


def embed_output(text: str) -> List[float]:
    client = ClientV2(api_key=os.environ.get("COHERE_API_KEY", ""))
    result = client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return list(result.embeddings[0])
