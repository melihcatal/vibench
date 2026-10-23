import google.generativeai as genai
import os
from typing import List
from storage_models import EmbeddingRequest

def get_text_embedding(request: EmbeddingRequest) -> List[float]:
    """Embeds object metadata and extracted text for search using Google Gemini Embeddings.

    Args:
        request: An EmbeddingRequest object.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure GOOGLE_API_KEY environment variable is set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    result = genai.embed_content(
        model=request.model_name,
        content=request.text_content,
        task_type="RETRIEVAL_DOCUMENT"
    )

    embedding = result['embedding']
    print(f"Generated embedding (model: {request.model_name}) for text of length {len(request.text_content)}")
    # print(f"Embedding: {embedding[:5]}...") # Print first 5 dimensions for brevity
    return embedding

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_API_KEY environment variable is set.
    # text_to_embed = "This is a document about cloud storage and data management."
    # embed_req = EmbeddingRequest(text_content=text_to_embed)
    # embedding_vector = get_text_embedding(embed_req)
    # print(f"Embedding vector length: {len(embedding_vector)}")

    # text_to_embed_2 = "Another document discussing scalable object storage solutions."
    # embed_req_2 = EmbeddingRequest(text_content=text_to_embed_2)
    # embedding_vector_2 = get_text_embedding(embed_req_2)
    # print(f"Embedding vector length: {len(embedding_vector_2)}")
    pass
