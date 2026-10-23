import google.generativeai as genai
import os

def embed_model_output(text: str) -> list[float]:
    """
    Embeds model output using Google's Generative AI embedding model.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # For clustering or retrieval, a general-purpose embedding model is suitable.
    # The 'embedding-001' model is a common choice for such tasks.
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="RETRIEVAL_DOCUMENT" # or "CLUSTERING", "SEMANTIC_SIMILARITY", etc. depending on exact use case
    )
    return response['embedding']

if __name__ == '__main_frame__':
    # Example usage:
    # Set your GOOGLE_API_KEY environment variable before running.
    # For example: export GOOGLE_API_KEY="your_api_key_here"
    sample_text = "This is an example model output that needs to be embedded."
    try:
        embedding = embed_model_output(sample_text)
        print(f"Embedding for '{sample_text[:50]}...': {embedding[:10]}...") # Print first 10 dimensions
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
