import os
import json
from google.cloud import generativemodel

# Use Gemini model for embeddings (requires GOOGLE_API_KEY env var)
def embed_log_messages(messages: list[str], model: str = 'gemini-1.5-flash-001') -> list[list[float]]:
    """Generates embeddings for each log message using Gemini API.

    Args:
        messages (List[str]): List of log message strings.
        model (str): Gemini model supporting embeddings.
    Returns:
        List of embedding vectors (list of floats) corresponding to each message.
    """
    client = generative_model.GenerativeModel(model)
    response = client.embed_content(messages)
    # Each embedding is under .embedding field
    return [entry.embedding for entry in response]

# Example usage (omit for library)
if __name__ == '__main__':
    vecs = embed_log_messages(['User login failed', 'Payment processed successfully'])
    print('Embeddings:', vecs)
