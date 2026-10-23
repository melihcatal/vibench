import os
from typing import Dict, List

from cohere import ClientV2


def embed_log_messages(messages: List[str]) -> Dict[str, object]:
    client = ClientV2(api_key=os.getenv("COHERE_API_KEY", ""))
    response = client.embed(
        model="embed-english-v3.0", texts=messages, input_type="search_document"
    )
    return {"embeddings": response.embeddings.float, "model": "embed-english-v3.0"}
