
import os
from document_client import get_azure_openai_client
from typing import List

def get_text_embedding(text: str) -> List[float]:
    client = get_azure_openai_client()
    deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002") # Default deployment

    response = client.embeddings.create(
        model=deployment_name,
        input=[text]
    )

    if response.data:
        return response.data[0].embedding
    return []
