import os
from typing import List, Dict, Any

import google.generativeai as genai

def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[List[float]]]:
    """Embeds a query and documents for semantic search using Google's Generative AI.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A dictionary containing 'query_embedding' and 'document_embeddings'.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("embedding-001")

    query_embedding = model.embed_content(content=query)["embedding"]
    document_embeddings = model.embed_content(content=documents)
    
    return {
        "query_embedding": query_embedding,
        "document_embeddings": [item["embedding"] for item in document_embeddings["embeddings"]]
    }

