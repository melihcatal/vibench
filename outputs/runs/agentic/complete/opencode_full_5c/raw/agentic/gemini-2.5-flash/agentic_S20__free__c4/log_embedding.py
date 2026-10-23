from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogEmbedding


def embed_log_messages(log_messages: List[str]) -> List[LogEmbedding]:
    """Embeds selected log messages for semantic retrieval using Google Cloud Vertex AI's text-embedding-gecko model.

    Args:
        log_messages: A list of log message strings to embed.

    Returns:
        A list of LogEmbedding objects, each containing the original text and its embedding vector.
    """
    client = ObservabilityClient()
    embeddings: List[LogEmbedding] = []

    if not log_messages:
        return embeddings

    try:
        # Vertex AI's text-embedding-gecko model expects a list of text inputs
        # The predict method returns a list of Endpoint.Prediction instances
        response = client.embedding_model.predict(instances=log_messages)

        # Each prediction object in response.predictions will have an 'embeddings' attribute
        # which is a list of floats (the embedding vector).
        for i, prediction_output in enumerate(response.predictions):
            original_text = log_messages[i]
            embedding_vector = prediction_output[
                "embeddings"
            ]  # This is a list of floats
            embeddings.append(LogEmbedding(original_text, embedding_vector))

    except Exception as e:
        print(f"Error during embedding generation: {e}")
        # In case of an error, return original messages with an empty embedding
        for message in log_messages:
            embeddings.append(LogEmbedding(message, []))

    return embeddings


if __name__ == "__main__":
    # Example usage
    log_messages_to_embed = [
        "User authentication failed with invalid credentials.",
        "Attempted login with incorrect password for user 'john.doe'.",
        "Database connection pool exhausted, unable to get a connection.",
        "SQL query timeout for orders table due to heavy load.",
        "Application started successfully on port 8080.",
    ]

    log_embeddings = embed_log_messages(log_messages_to_embed)

    print("\n--- Log Message Embeddings ---")
    for log_embed in log_embeddings:
        print(f"Original Text: '{log_embed.original_text}'")
        print(f"Embedding (first 5 values): {log_embed.embedding[:5]}...")
        print(f"Embedding Dimension: {len(log_embed.embedding)}\n")

    # Example of how you might use embeddings for semantic similarity (conceptual)
    # from scipy.spatial.distance import cosine

    # if len(log_embeddings) >= 2:
    #     embed1 = log_embeddings[0].embedding
    #     embed2 = log_embeddings[1].embedding
    #     embed3 = log_embeddings[2].embedding

    #     print(f"Cosine similarity between '{log_embeddings[0].original_text}' and '{log_embeddings[1].original_text}': {1 - cosine(embed1, embed2)}")
    #     print(f"Cosine similarity between '{log_embeddings[0].original_text}' and '{log_embeddings[2].original_text}': {1 - cosine(embed1, embed3)}")
