import google.generativeai as genai
import os
import numpy as np

def get_text_embedding(text: str) -> list[float]:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    
    genai.configure(api_key=google_api_key)

    # Use a specific embedding model
    model_name = "models/embedding-001"

    try:
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error calling Gemini Embeddings API: {e}")
        return []

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set as an environment variable

    caption_chunk_1 = "The marketing team discussed the Q3 strategy and influencer campaigns."
    embedding_1 = get_text_embedding(caption_chunk_1)
    print(f"Caption 1: '{caption_chunk_1}'\nEmbedding length: {len(embedding_1)}\n")
    # print(f"Embedding 1: {embedding_1[:5]}...") # Print first 5 elements for brevity

    caption_chunk_2 = "Engineering sprint review completed, focusing on feature release 1.2 and bug fixes."
    embedding_2 = get_text_embedding(caption_chunk_2)
    print(f"Caption 2: '{caption_chunk_2}'\nEmbedding length: {len(embedding_2)}\n")

    caption_chunk_3 = "The sales figures for the last quarter were encouraging, exceeding targets by 10%."
    embedding_3 = get_text_embedding(caption_chunk_3)
    print(f"Caption 3: '{caption_chunk_3}'\nEmbedding length: {len(embedding_3)}\n")

    # Example of calculating cosine similarity (for semantic search illustration)
    if embedding_1 and embedding_2:
        dot_product = np.dot(embedding_1, embedding_2)
        norm_a = np.linalg.norm(embedding_1)
        norm_b = np.linalg.norm(embedding_2)
        if norm_a > 0 and norm_b > 0:
            similarity = dot_product / (norm_a * norm_b)
            print(f"Cosine similarity between Caption 1 and Caption 2: {similarity:.4f}")

    if embedding_1 and embedding_3:
        dot_product = np.dot(embedding_1, embedding_3)
        norm_a = np.linalg.norm(embedding_1)
        norm_b = np.linalg.norm(embedding_3)
        if norm_a > 0 and norm_b > 0:
            similarity = dot_product / (norm_a * norm_b)
            print(f"Cosine similarity between Caption 1 and Caption 3: {similarity:.4f}")
