import google.generativeai as genai
import os
from typing import List

def initialize_gemini_embeddings():
    """Initializes the Google Gemini API client for embeddings."""
    if "GOOGLE_API_KEY" not in os.environ:
        print("Warning: GOOGLE_API_KEY environment variable not set.")
        print("Please set your GOOGLE_API_KEY to use the Gemini Embeddings API.")
        return None
    
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    # The embedding model is typically specified directly in the embedding call.
    return True # Return True if configuration is successful

def embed_caption_chunk(caption_chunk: str) -> List[float]:
    """Generates an embedding for a single caption chunk using Google Gemini Embeddings.

    Args:
        caption_chunk: The text chunk to embed.

    Returns:
        A list of floats representing the embedding vector.
        Returns an empty list if an error occurs or API key is not set.
    """
    if not caption_chunk.strip():
        return []
    
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY is not set for embedding.")
        return []

    try:
        # Use the 'embedding-001' model for text embeddings
        response = genai.embed_content(
            model='models/embedding-001',
            content=caption_chunk,
            task_type="RETRIEVAL_DOCUMENT" # or other relevant task type
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []

if __name__ == "__main__":
    print("Initializing Gemini Embeddings...")
    if initialize_gemini_embeddings():
        print("\n--- Embedding sample caption chunks ---")

        caption1 = "The project deadline has been extended by two weeks."
        embedding1 = embed_caption_chunk(caption1)
        if embedding1:
            print(f"Caption 1: '{caption1}'")
            print(f"Embedding 1 (first 5 dimensions): {embedding1[:5]}...")
            print(f"Embedding 1 length: {len(embedding1)}\n")

        caption2 = "We need to submit the final report by Friday."
        embedding2 = embed_caption_chunk(caption2)
        if embedding2:
            print(f"Caption 2: '{caption2}'")
            print(f"Embedding 2 (first 5 dimensions): {embedding2[:5]}...")
            print(f"Embedding 2 length: {len(embedding2)}\n")

        caption3 = "The project delivery date has been moved to next month."
        embedding3 = embed_caption_chunk(caption3)
        if embedding3:
            print(f"Caption 3: '{caption3}'")
            print(f"Embedding 3 (first 5 dimensions): {embedding3[:5]}...")
            print(f"Embedding 3 length: {len(embedding3)}\n")

        # You can then use these embeddings for similarity search, e.g., using a vector database.
    else:
        print("Gemini Embeddings not available. Skipping embedding demonstration.")
