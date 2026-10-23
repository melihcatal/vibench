import os
from google.cloud import aiplatform


def embed_log_message(
    log_message: str, project_id: str, location: str = "us-central1"
) -> list[float]:
    """
    Generates a text embedding for a log message using Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)

    # Use a specific Vertex AI text embedding model
    model_name = "textembedding-gecko@001"

    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)

    embeddings = model.get_embeddings([log_message])

    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return []


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if gcp_project_id:
        message_to_embed = "CRITICAL: Database primary node is unresponsive. Failing over to secondary."

        embedding_vector = embed_log_message(
            message_to_embed, project_id=gcp_project_id
        )

        print(f"Generated embedding for: '{message_to_embed}'")
        print(f"Vector dimensions: {len(embedding_vector)}")
        # Print first 5 dimensions as a sample
        print(f"Sample of vector: {embedding_vector[:5]}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
