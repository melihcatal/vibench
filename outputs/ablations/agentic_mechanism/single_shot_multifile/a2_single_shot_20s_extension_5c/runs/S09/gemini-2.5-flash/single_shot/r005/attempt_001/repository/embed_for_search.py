import os
import voyageai
from typing import List, Dict

def embed_query_and_documents(query_text: str, document_texts: List[str], model: str = "voyage-large-2") -> Dict[str, List[List[float]]]:
    api_key = os.getenv("VOYAGE_API_KEY")
    if not api_key:
        raise ValueError("VOYAGE_API_KEY environment variable not set.")
    
    client = voyageai.Client(api_key=api_key)
    
    query_response = client.embed(query_text, model=model, input_type="query")
    query_embedding = query_response.embeddings[0]
    
    document_response = client.embed(document_texts, model=model, input_type="document")
    document_embeddings = document_response.embeddings
    
    return {
        "query_embedding": [query_embedding],
        "document_embeddings": document_embeddings
    }
