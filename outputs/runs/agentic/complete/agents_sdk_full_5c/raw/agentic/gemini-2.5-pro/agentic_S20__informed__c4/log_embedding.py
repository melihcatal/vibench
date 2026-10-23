import os
import cohere
from typing import List, Union

def embed_log_message(text_to_embed: Union[str, List[str]]) -> dict:
    """
    Embeds selected log messages for semantic retrieval using Cohere.

    Args:
        text_to_embed: A single log message string or a list of strings.

    Returns:
        A dictionary containing the embeddings or an error.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        texts = [text_to_embed] if isinstance(text_to_embed, str) else text_to_embed
        
        response = co.embed(
            texts=texts,
            model="embed-english-light-v3.0",
            input_type="search_document"
        )
        
        return {
            "embeddings": response.embeddings,
            "model": "embed-english-light-v3.0",
        }

    except cohere.core.api_error.ApiError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return {"error": str(e)}


# Example of how this might be called (not executed):
# if __name__ == '__main__':
#     log_message = "Database connection timed out after 30 seconds."
#     embedding_result = embed_log_message(log_message)
#
#     if "embeddings" in embedding_result:
#         # In a real app, you would store this vector in a vector database.
#         print(f"Successfully generated embedding vector of dimension: {len(embedding_result['embeddings'][0])}")
#     else:
#         print(f"Failed to generate embedding: {embedding_result.get('error')}")
