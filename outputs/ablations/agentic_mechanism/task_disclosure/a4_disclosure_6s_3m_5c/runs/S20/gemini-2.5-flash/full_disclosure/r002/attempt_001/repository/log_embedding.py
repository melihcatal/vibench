import openai
import os

def embed_log_messages(log_messages: list[str]) -> list[list[float]]:
    """
    Embeds a list of log messages using OpenAI's embedding service for semantic retrieval.

    Args:
        log_messages: A list of log messages (strings) to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    # Initialize OpenAI client with API key from environment variable
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # OpenAI's recommended embedding model for many use cases
    model = "text-embedding-ada-002"

    embeddings = []
    for message in log_messages:
        try:
            response = client.embeddings.create(input=[message], model=model)
            embeddings.append(response.data[0].embedding)
        except Exception as e:
            print(f"Error embedding message: {message} - {e}")
            embeddings.append([]) # Append an empty list or handle the error as appropriate

    return embeddings
