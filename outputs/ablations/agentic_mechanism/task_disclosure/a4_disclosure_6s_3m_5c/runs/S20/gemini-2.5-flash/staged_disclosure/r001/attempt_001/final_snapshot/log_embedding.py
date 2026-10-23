import os
from openai import OpenAI

def embed_log_message(log_message: str) -> list[float]:
    """
    Embeds a single log message using OpenAI's embedding API.

    Args:
        log_message: The log message to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=[log_message],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    test_message = "User login failed due to incorrect password."
    embedding = embed_log_message(test_message)
    print(f"Log message: '{test_message}'")
    print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding length: {len(embedding)}")
