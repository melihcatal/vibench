import os
from observability_client import get_gemini_model


def embed_log_messages(log_messages: list[str]) -> list[list[float]]:
    """
    Embeds selected log messages for semantic retrieval using the Google Gemini Embeddings API.
    """
    model = get_gemini_model(
        "embedding-001"
    )  # embedding-001 is a provider-specific model ID

    # The Gemini API's embed_content method accepts a list of texts for batch embedding.
    # It returns a list of embedding objects, each containing an array of floats.
    response = model.embed_content(log_messages)

    embeddings = [item.embedding for item in response.embeddings]
    return embeddings


if __name__ == "__main__":
    sample_log_messages = [
        "User login failed from IP 192.168.1.10",
        "Successful login for administrator user.",
        "Database connection timed out after 30 seconds.",
        "Error: Unable to connect to PostgreSQL.",
        "Application started successfully.",
        "Server reboot initiated by system user.",
    ]

    embeddings = embed_log_messages(sample_log_messages)

    print(f"Generated {len(embeddings)} embeddings.")
    for i, embedding in enumerate(embeddings):
        print(f"Message '{sample_log_messages[i]}' embedding length: {len(embedding)}")
        print(
            f"First 5 dimensions: {embedding[:5]}..."
        )  # Print first few dimensions for brevity
