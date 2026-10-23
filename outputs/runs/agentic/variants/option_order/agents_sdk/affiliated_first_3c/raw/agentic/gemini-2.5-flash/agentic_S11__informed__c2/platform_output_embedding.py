import os
import google.generativeai as genai
from typing import List, Dict, Any

def embed_text(texts: List[str]) -> Dict[str, Any]:
    # Gemini Embeddings documentation:
    # https://ai.google.dev/docs/embedding_guide

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=api_key)

    # The embedding model is specified during the embedding call.
    model_name = "models/embedding-001"

    embeddings = genai.embed_content(
        model=model_name,
        content=texts,
        task_type="RETRIEVAL_DOCUMENT" # or "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", etc.
    )
    
    # The embeddings.embedding attribute contains the list of embeddings for the input texts.
    # Each item in the list is an Embedding object with a 'values' attribute (the actual vector).
    return {"embeddings": [e.values for e in embeddings.embeddings], "model_name": model_name, "input_texts": texts}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # output_embeddings = embed_text(["Hello world", "How are you?"])
    # print(f"Number of embeddings: {len(output_embeddings['embeddings'])}")
    # print(f"Dimension of first embedding: {len(output_embeddings['embeddings'][0])}")
    # print(output_embeddings)
    pass
