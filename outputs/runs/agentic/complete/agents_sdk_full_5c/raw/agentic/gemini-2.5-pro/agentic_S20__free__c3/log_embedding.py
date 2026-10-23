import os
import cohere
from typing import List, Union

def get_log_embeddings(log_messages: List[str]) -> Union[List[List[float]], None]:
    """
    Generates embeddings for a list of log messages using the Cohere API.

    Args:
        log_messages: A list of string messages to embed.

    Returns:
        A list of embedding vectors, or None if an error occurs.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        print("Error: COHERE_API_KEY environment variable not set.")
        return None

    if not log_messages:
        return []

    try:
        co = cohere.Client(api_key)

        response = co.embed(
            texts=log_messages,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        return response.embeddings

    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
