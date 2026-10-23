import openai
from document_client import get_openai_client
from typing import List

def get_ocr_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Embeds extracted document sections for semantic retrieval using OpenAI Embeddings.
    """
    client = get_openai_client()
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    # The embedding is usually a list of floats
    return response.data[0].embedding
