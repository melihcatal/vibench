import os
from openai import OpenAI


def embed_script(text: str) -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    try:
        # The model to use for embeddings. 'text-embedding-ada-002' is a common choice.
        # For newer models like 'text-embedding-3-small' or 'text-embedding-3-large',
        # you might need to specify dimensions.
        response = client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"OpenAI embedding creation failed: {e}")


if __name__ == "__main__":
    # Example usage
    os.environ["OPENAI_API_KEY"] = (
        "YOUR_OPENAI_API_KEY"  # Replace with actual key for testing
    )
    # try:
    #     embedding = embed_script("This is a sample narration script.")
    #     print(f"Embedding (first 5 values): {embedding[:5]}...")
    #     print(f"Embedding length: {len(embedding)}")
    # except Exception as e:
    #     print(f"Embedding error: {e}")
