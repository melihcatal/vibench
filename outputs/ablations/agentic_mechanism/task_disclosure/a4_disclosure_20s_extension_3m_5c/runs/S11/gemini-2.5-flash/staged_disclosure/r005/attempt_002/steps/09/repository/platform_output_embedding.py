import openai
import os

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs using OpenAI's embedding model.
    The OpenAI API key is expected to be set as an environment variable named OPENAI_API_KEY.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        model="text-embedding-ada-002",  # Concrete model identifier
        input=[text]
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    # Set your OpenAI API key as an environment variable:
    # export OPENAI_API_KEY="your_openai_api_key_here"
    #
    # Then run this script:
    # python platform_output_embedding.py

    sample_output = "This is a sample platform output to be embedded."
    try:
        embedding = embed_platform_output(sample_output)
        print(f"Embedding for the sample output (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding length: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
