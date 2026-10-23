import os
from openai import OpenAI


def embed_log_messages(log_messages: list[str]) -> list[list[float]]:
    """
    Creates embeddings for a list of log messages using the OpenAI API.

    Args:
        log_messages: A list of strings, where each string is a log message.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=log_messages, model="text-embedding-3-small"
        )
        return [embedding.embedding for embedding in response.data]
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return []


if __name__ == "__main__":
    if os.environ.get("OPENAI_API_KEY"):
        messages = [
            "User authentication failed: invalid password for user 'admin'.",
            "Database connection timeout: unable to connect to primary DB.",
            "User authentication successful for user 'jane.doe'.",
            "Failed to connect to database replica.",
        ]

        embeddings = embed_log_messages(messages)

        if embeddings:
            print(f"Successfully generated {len(embeddings)} embeddings.")
            print(f"Dimension of first embedding: {len(embeddings[0])}")
            # print("First embedding (truncated):", embeddings[0][:5])
    else:
        print("OPENAI_API_KEY not set. Skipping example run.")
