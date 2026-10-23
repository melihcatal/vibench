import os
import google.generativeai as genai

def embed_caption_chunk(caption_chunk: str) -> list[float]:
    # Configure the Google Gemini API
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Please set the GOOGLE_API_KEY environment variable.")
        return []
    genai.configure(api_key=api_key)

    # The embedding model to use
    # As of now, 'models/embedding-001' is a common choice for text embeddings.
    # Check Google's documentation for the latest recommended embedding models.
    model_name = "models/embedding-001"

    try:
        response = genai.embed_content(model=model_name, content=caption_chunk)
        embedding = response['embedding']
        print(f"Embedding for \'{caption_chunk}\' generated (length: {len(embedding)}).")
        return embedding
    except Exception as e:
        print(f"An error occurred during embedding with Gemini API: {e}")
        return []

if __name__ == "__main__":
    # Set GOOGLE_API_KEY environment variable for authentication

    example_caption = "The quick brown fox jumps over the lazy dog."
    embedding_vector = embed_caption_chunk(example_caption)
    if embedding_vector:
        print(f"First 5 dimensions of embedding: {embedding_vector[:5]}")

    print("\n--- Testing another caption ---")
    another_caption = "A fast reddish-brown canid leaps above a sluggish canine."
    another_embedding_vector = embed_caption_chunk(another_caption)
    if another_embedding_vector:
        print(f"First 5 dimensions of embedding: {another_embedding_vector[:5]}")

    print("\n--- Testing a semantically different caption ---")
    different_caption = "The capital of France is Paris."
    different_embedding_vector = embed_caption_chunk(different_caption)
    if different_embedding_vector:
        print(f"First 5 dimensions of embedding: {different_embedding_vector[:5]}")

    # In a real application, you would store these embeddings in a vector database
    # and perform similarity searches.
