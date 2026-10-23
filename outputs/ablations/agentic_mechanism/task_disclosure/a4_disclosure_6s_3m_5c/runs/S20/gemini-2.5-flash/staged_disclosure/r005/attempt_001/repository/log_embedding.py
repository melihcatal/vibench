
import os
from openai import OpenAI

def get_log_embedding(log_message: str) -> list[float]:
    """
    Embeds a given log message using OpenAI's embedding model for semantic retrieval.

    Args:
        log_message: The log message to embed.

    Returns:
        A list of floats representing the embedding of the log message.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    response = client.embeddings.create(
        input=log_message,
        model="text-embedding-ada-002"  # Concrete OpenAI embedding model
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage (requires OPENAI_API_KEY environment variable to be set)
    # To run this example, first set your OpenAI API key:
    # export OPENAI_API_KEY="your_openai_api_key_here"

    sample_log = "User login failed due to incorrect password."
    embedding = get_log_embedding(sample_log)
    print(f"Log message: '{sample_log}'")
    print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding length: {len(embedding)}")

    sample_log_2 = "Failed attempt to authenticate user from IP 192.168.1.1"
    embedding_2 = get_log_embedding(sample_log_2)
    print(f"Log message: '{sample_log_2}'")
    print(f"Embedding (first 5 dimensions): {embedding_2[:5]}...")
    print(f"Embedding length: {len(embedding_2)}")
