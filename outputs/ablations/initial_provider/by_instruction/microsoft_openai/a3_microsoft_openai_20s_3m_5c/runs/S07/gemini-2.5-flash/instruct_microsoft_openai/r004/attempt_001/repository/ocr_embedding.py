from document_client import get_openai_client
import os

def embed_text(text: str) -> list[float]:
    client = get_openai_client()
    
    response = client.embeddings.create(
        input=text,
        model=os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002"), # Use deployment name
    )
    
    return response.data[0].embedding
