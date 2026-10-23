import os
import openai

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs using OpenAI's text-embedding-ada-002 model.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure the OpenAI API key is set as an environment variable
    # For example: export OPENAI_API_KEY="YOUR_API_KEY"
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Use the concrete external provider (OpenAI) and model (text-embedding-ada-002)
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_output = "This is an example platform output that needs to be embedded for evaluation."
    try:
        embedding = embed_platform_output(example_output)
        print(f"Embedding successful. Vector length: {len(embedding)}")
        # print(f"First 5 dimensions of the embedding: {embedding[:5]}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the OPENAI_API_KEY environment variable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
