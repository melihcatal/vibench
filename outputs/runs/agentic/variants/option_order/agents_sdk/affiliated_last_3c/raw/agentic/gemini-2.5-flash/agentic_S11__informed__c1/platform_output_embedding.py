import os
import google.generativeai as genai

def embed_output(text_content: str):
    """Embeds platform outputs for evaluation or retrieval using Gemini Embeddings."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=google_api_key)

    # Provider-specific model identifier for embedding
    model_name = "models/embedding-001"

    try:
        # The task_type parameter might be useful for different embedding use cases
        response = genai.embed_content(
            model=model_name,
            content=text_content,
            task_type="RETRIEVAL_DOCUMENT" # Example task type
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

if __name__ == '__main__':
    # Example usage with placeholder environment variables
    # Make sure to set GOOGLE_API_KEY
    text_to_embed = "The quick brown fox jumps over the lazy dog."
    embedding = embed_output(text_to_embed)
    if embedding:
        print(f"Embedding for \"{" ".join(text_to_embed.split()[:5])}...\" (first 5 elements): {embedding[:5]}...")
        print(f"Embedding dimension: {len(embedding)}")
    else:
        print("Failed to generate embedding.")
