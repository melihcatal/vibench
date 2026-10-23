from google.cloud import aiplatform

def embed_moderation_rationale(text: str) -> list[float]:
    """Embeds moderation rationale text for case retrieval using Vertex AI.

    Args:
        text: The moderation rationale text to embed.

    Returns:
        A list of floats representing the embedding of the text.
    """
    client = aiplatform.gapic.PredictionServiceClient()
    project = "your-gcp-project-id"  # Replace with your GCP project ID
    location = "us-central1"  # Replace with your desired region
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/text-embedding-004"

    instance = aiplatform.gapic.PredictRequest(
        endpoint=endpoint,
        instances=[{"content": text}],
    )
    response = client.predict(request=instance)
    embedding = response.predictions[0]["embeddings"]["values"]
    return embedding
