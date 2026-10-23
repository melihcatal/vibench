import os
from google.cloud import aiplatform

def embed_audit_note(project_id: str, location: str, audit_note: str) -> list[float]:
    """
    Embeds a crypto audit note using Google Cloud Vertex AI's textembedding-gecko model.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        audit_note: The text of the audit note to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.gapic.PredictionServiceClient()
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/textembedding-gecko"

    instance = aiplatform.gapic.instance.TextEmbeddingPredictionInstance(content=audit_note).to_value()
    instances = [instance]
    parameters = aiplatform.gapic.types.SimilarityPredictionModel.PredictRequest.query_parameters(
        dimension=768
    )

    response = model.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    embedding = [float(value) for value in response.predictions[0]["embeddings"]["values"]]
    return embedding

if __name__ == "__main__":
    # Example Usage:
    # Ensure you have authenticated with Google Cloud (e.g., gcloud auth application-default login)
    # and set the GOOGLE_CLOUD_PROJECT environment variable.
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise EnvironmentError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    
    location = "us-central1"  # Or your desired region
    
    note_1 = "Review of smart contract for reentrancy vulnerabilities."
    note_2 = "Audit of cryptographic key rotation policies."
    note_3 = "Security assessment of a new financial application."

    embedding_1 = embed_audit_note(project_id, location, note_1)
    print(f"Embedding for note 1 (first 5 dimensions): {embedding_1[:5]}")

    embedding_2 = embed_audit_note(project_id, location, note_2)
    print(f"Embedding for note 2 (first 5 dimensions): {embedding_2[:5]}")

    embedding_3 = embed_audit_note(project_id, location, note_3)
    print(f"Embedding for note 3 (first 5 dimensions): {embedding_3[:5]}")
