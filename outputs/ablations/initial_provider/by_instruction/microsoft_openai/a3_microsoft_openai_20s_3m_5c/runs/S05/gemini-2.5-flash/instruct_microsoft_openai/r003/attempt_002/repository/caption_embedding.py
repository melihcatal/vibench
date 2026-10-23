import os
import cohere

cohere_client = cohere.Client(os.environ.get("COHERE_API_KEY"))

def embed_caption_chunk(caption_chunk: str) -> list[float]:
    try:
        response = cohere_client.embed(
            texts=[caption_chunk],
            model="embed-english-v3.0" # Using a specific Cohere embed model
        )
        return response.embeddings[0]
    except Exception as e:
        print(f"Error embedding caption chunk: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    sample_caption = "The quick brown fox jumps over the lazy dog."
    embedding = embed_caption_chunk(sample_caption)
    print(f"Caption: \"{sample_caption}\"")
    print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding length: {len(embedding)}")
