import google.generativeai as genai
import os
from typing import List

def get_text_embedding(text: str, model_name: str = "models/embedding-001") -> List[float]:
    """Embeds narration scripts for voice-asset search using Google Gemini Embeddings.

    Args:
        text: The text content to embed.
        model_name: The name of the embedding model (e.g., "models/embedding-001").
                    Ensure this model is supported for text embeddings.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure GOOGLE_API_KEY environment variable is set.
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")) # This should be configured once globally or per client

    try:
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []


if __name__ == '__main__':
    # Before running, ensure you have set your GOOGLE_API_KEY environment variable
    # e.g., os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

    # if os.environ.get("GOOGLE_API_KEY"):
    #     script_part_1 = "The quick brown fox jumps over the lazy dog."
    #     embedding_1 = get_text_embedding(script_part_1)
    #     print(f"Embedding for \'{script_part_1}\' (first 5 dims): {embedding_1[:5]}...")

    #     script_part_2 = "A fast reddish-brown canine leaps above a lethargic hound."
    #     embedding_2 = get_text_embedding(script_part_2)
    #     print(f"Embedding for \'{script_part_2}\' (first 5 dims): {embedding_2[:5]}...")

    #     # You would typically calculate similarity between embeddings here
    # else:
    #     print("Please set the GOOGLE_API_KEY environment variable to run embedding example.")

    print("\nSimulated embedding generation. Set GOOGLE_API_KEY to run actual embedding.")
    print("Embedding (first 5 dims): [0.1, 0.2, 0.3, 0.4, 0.5]...")
