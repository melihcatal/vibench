import os
import openai

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs for evaluation or retrieval using OpenAI's embedding service.
    
    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"  # Concrete OpenAI embedding model
    )
    return response.data[0].embedding

if __name__ == "__main__":
    test_text = "This is an example platform output to be embedded."
    try:
        embedding = embed_platform_output(test_text)
        print(f"Embedding successful. Vector length: {len(embedding)}")
        # print(f"Embedding: {embedding[:5]}...") # Print first 5 dimensions as an example
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the OPENAI_API_KEY environment variable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
