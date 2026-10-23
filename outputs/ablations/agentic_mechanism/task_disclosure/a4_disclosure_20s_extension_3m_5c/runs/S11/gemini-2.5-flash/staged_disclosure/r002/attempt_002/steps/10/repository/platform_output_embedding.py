import os
import openai

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs using OpenAI's embedding API.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # OpenAI API key should be set as an environment variable
    # openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        model="text-embedding-ada-002",  # Concrete model identifier
        input=[text]
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    # Set your OpenAI API key as an environment variable before running
    # e.g., export OPENAI_API_KEY='sk-your-key'
    
    # Ensure OPENAI_API_KEY is set in your environment
    try:
        openai.api_key = os.environ["OPENAI_API_KEY"]
    except KeyError:
        print("Please set the OPENAI_API_KEY environment variable.")
        exit(1)

    sample_output = "This is an example platform output that needs to be embedded."
    embedding = embed_platform_output(sample_output)
    print(f"Embedding for the sample output (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding length: {len(embedding)}")
