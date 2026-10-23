import google.generativeai as genai
import os
from typing import List

def get_text_embedding(text: str) -> List[float]:
    """Generates embeddings for a given text using Google's Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set.
    # genai.configure(api_key="YOUR_API_KEY") if not set in env
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    model = genai.GenerativeModel('gemini-pro') # Using a suitable generative model for embedding
    
    # The embedding model is usually a separate one, e.g., embedding-001
    # However, if genai.embed_content is available, it's more direct.
    # For this example, let's assume 'embedding-001' or similar is the target.
    # If `genai.embed_content` is available and configured, that is the direct way.
    # As of current genai SDK, embed_content is the standard for embeddings.
    
    try:
        # Using the standard embedding API from google-genai
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Fallback/alternative if embed_content requires a different setup or is not direct
        # This part might vary based on the exact version/configuration of the genai lib
        # For simpler examples, sometimes generative models also offer embedding features
        # via their generate_content (though less optimized for pure embedding tasks)
        return []

if __name__ == "__main__":
    if "GOOGLE_API_KEY" not in os.environ:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        try:
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            text_to_embed = "This is a narration script about historical events."
            embedding = get_text_embedding(text_to_embed)
            if embedding:
                print(f"Embedding for '{text_to_embed}' (first 5 dimensions): {embedding[:5]}...")
                print(f"Embedding dimension: {len(embedding)}")
            else:
                print("Failed to get embedding.")

            text_to_embed_2 = "Another script talking about science and technology."
            embedding_2 = get_text_embedding(text_to_embed_2)
            if embedding_2:
                print(f"\nEmbedding for '{text_to_embed_2}' (first 5 dimensions): {embedding_2[:5]}...")

        except Exception as e:
            print(f"An error occurred during main execution: {e}")
