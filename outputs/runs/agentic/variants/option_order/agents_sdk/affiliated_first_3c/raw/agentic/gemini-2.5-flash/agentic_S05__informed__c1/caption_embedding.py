import os
import google.generativeai as genai
from typing import List

def embed_caption_chunk(caption_chunk: str, model_name: str = "models/embedding-001") -> List[float]:
    """Generates embeddings for a given caption chunk using Google Gemini Embeddings.

    Args:
        caption_chunk (str): The text chunk to embed.
        model_name (str): The name of the embedding model to use (e.g., "models/embedding-001").

    Returns:
        List[float]: A list of floats representing the embedding vector.

    Raises:
        Exception: If the API call fails or the GOOGLE_API_KEY is not set.
    """
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    try:
        response = genai.embed_content(
            model=model_name,
            content=caption_chunk,
            task_type="RETRIEVAL_DOCUMENT" # Specify task type for better embeddings
        )
        embedding = response["embedding"]
        print(f"Caption: '{caption_chunk[:50]}...'")
        print(f"Embedding dimension: {len(embedding)}")
        # print(f"Embedding: {embedding[:5]}...") # Print a snippet for brevity
        return embedding

    except Exception as e:
        print(f"Error generating embedding with Gemini API: {e}")
        return []

if __name__ == "__main__":
    # To run this, ensure GOOGLE_API_KEY is set.
    # export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    print("Caption embedding for semantic meeting search using Google Gemini Embeddings.")

    caption_1 = "The discussion focused on increasing user engagement by 20% next quarter."
    caption_2 = "We need to improve the user experience to achieve our engagement goals."
    caption_3 = "The financial report shows a slight decline in revenue for the last month."

    try:
        print("\n--- Embedding Caption 1 ---")
        embedding_1 = embed_caption_chunk(caption_1)
        
        print("\n--- Embedding Caption 2 ---")
        embedding_2 = embed_caption_chunk(caption_2)

        print("\n--- Embedding Caption 3 ---")
        embedding_3 = embed_caption_chunk(caption_3)

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    print("Ensure GOOGLE_API_KEY is set for execution.")
