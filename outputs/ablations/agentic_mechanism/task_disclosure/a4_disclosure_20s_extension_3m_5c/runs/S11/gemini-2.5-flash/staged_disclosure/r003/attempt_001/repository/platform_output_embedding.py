import os
import openai

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs using OpenAI's embedding model.

    Args:
        text: The text content to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    try:
        # Ensure the OpenAI API key is set as an environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        client = openai.OpenAI(api_key=api_key)

        # Use a specific OpenAI embedding model
        response = client.embeddings.create(
            input=[text],
            model="text-embedding-ada-002"  # Concrete OpenAI model identifier
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error during embedding: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    platform_output_example = "This is an example platform output for embedding."
    embedding = embed_platform_output(platform_output_example)
    if embedding:
        print(f"Embedding for the output: {embedding[:5]}...") # Print first 5 elements
        print(f"Embedding length: {len(embedding)}")
    else:
        print("Failed to generate embedding.")
