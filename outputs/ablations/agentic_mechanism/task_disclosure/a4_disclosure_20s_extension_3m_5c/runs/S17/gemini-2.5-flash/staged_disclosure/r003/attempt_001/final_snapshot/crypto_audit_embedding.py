import openai
import os

def embed_text(text_to_embed: str) -> list[float]:
    """
    Embeds the given text using OpenAI's text-embedding-ada-002 model.

    Args:
        text_to_embed: The text content to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure the OpenAI API key is set
    # It's recommended to load this from environment variables or a secure configuration system
    # openai.api_key = os.getenv("OPENAI_API_KEY") 
    # For demonstration purposes, we assume openai.api_key is set elsewhere or
    # passed securely.

    if not text_to_embed:
        raise ValueError("Text to embed cannot be empty.")

    try:
        response = openai.embeddings.create(
            input=text_to_embed,
            model="text-embedding-ada-002"  # Concrete external provider and model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error during embedding: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    audit_note = "Review of smart contract for reentrancy vulnerabilities."
    try:
        embedding = embed_text(audit_note)
        print(f"Embedding for the audit note (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding length: {len(embedding)}")
    except ValueError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Please ensure your OPENAI_API_KEY environment variable is set.")
