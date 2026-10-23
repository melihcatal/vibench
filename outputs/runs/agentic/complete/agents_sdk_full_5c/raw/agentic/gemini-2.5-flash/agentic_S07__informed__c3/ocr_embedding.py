import os
import google.generativeai as genai

def embed_text(text: str) -> list:
    """
    Embeds the input text using Gemini Embeddings (via google-genai).
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # The model name for embeddings is typically 'embedding-001' or a specific variant
    # Ensure the model supports text embeddings.
    model = "models/embedding-001"

    try:
        response = genai.embed_content(
            model=model,
            content=text,
            task_type="RETRIEVAL_DOCUMENT" # Specify task type for better embeddings
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error embedding text: {e}")
        return []

if __name__ == '__main__':
    # Placeholder for direct execution
    # sample_text = "The quick brown fox jumps over the lazy dog."
    # embedding = embed_text(sample_text)
    # if embedding:
    #     print(f"Embedding (first 5 elements): {embedding[:5]}...")
    #     print(f"Embedding dimension: {len(embedding)}")
    pass
