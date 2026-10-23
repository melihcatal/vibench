import os
import google.generativeai as genai

def embed_platform_outputs(texts: list[str]) -> list[list[float]]:
    """Embeds platform outputs for evaluation or retrieval using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set for Gemini Embeddings.")

    genai.configure(api_key=api_key)

    model = "models/embedding-001" # Or other embedding model like "text-embedding-004"

    embeddings = []
    for text in texts:
        response = genai.embed_content(model=model, content=text)
        embeddings.append(response['embedding'])
    return embeddings

if __name__ == '__main__':
    # Example usage
    try:
        sample_texts = [
            "The cat sat on the mat.",
            "A feline rested on the rug.",
            "The dog chased the ball."
        ]
        text_embeddings = embed_platform_outputs(sample_texts)

        print(f"Generated {len(text_embeddings)} embeddings, each with dimension {len(text_embeddings[0])}.")
        print(f"Embedding for '{sample_texts[0]}': {text_embeddings[0][:5]}...") # Print first 5 dimensions
        print(f"Embedding for '{sample_texts[1]}': {text_embeddings[1][:5]}...")
        print(f"Embedding for '{sample_texts[2]}': {text_embeddings[2][:5]}...")

    except ValueError as e:
        print(f"Error: {e}. Please ensure GOOGLE_API_KEY is set.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
