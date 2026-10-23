import google.generativeai as genai
from observability_client import get_generative_model_client


def embed_log_message(log_message: str) -> list[float]:
    """
    Embeds a log message using Google's text embedding model.
    """
    # Note: get_generative_model_client is not used here because the embedding API
    # has a different initialization pattern in the google-generativeai library.
    # We still keep it in observability_client for other generative tasks.

    api_key = get_generative_model_client()._client._api_key
    if not api_key:
        raise ValueError("GEMINI_API_KEY not available for embedding client.")
    genai.configure(api_key=api_key)

    model_id = "models/text-embedding-004"

    result = genai.embed_content(
        model=model_id, content=log_message, task_type="RETRIEVAL_DOCUMENT"
    )

    return result["embedding"]


if __name__ == "__main__":
    message = "Database connection timed out for user 54321."
    embedding = embed_log_message(message)
    print(f"Generated embedding for the log message (first 10 dimensions):")
    print(embedding[:10])
    print(f"Total dimensions: {len(embedding)}")
