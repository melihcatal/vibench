from document_client import get_openai_client
from typing import List

def embed_text(text: str, model_name: str = "text-embedding-ada-002") -> List[float]:
    client = get_openai_client()

    # The embedding model deployment name is typically provided as a parameter to the API call
    response = client.embeddings.create(input=text, model=model_name)

    if response.data:
        return response.data[0].embedding
    return []
