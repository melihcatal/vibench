from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict

def embed_audit_notes(project_id: str, location: str, text: str) -> list[float]:
    """Embeds crypto audit notes using Google's Vertex AI Embedding API.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region of the Vertex AI endpoint (e.g., "us-central1").
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_endpoint = f"{location}-aiplatform.googleapis.com"
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # Use the 'text-embedding-004' model for embeddings
    model_id = "text-embedding-004"
    endpoint = client.endpoint_path(
        project=project_id, location=location, endpoint=model_id
    )

    instance = predict.instance.TextEmbeddingPredictionInstance(
        content=text
    ).to_value()
    instances = [instance]

    response = client.predict(endpoint=endpoint, instances=instances)
    
    embeddings = []
    for prediction in response.predictions:
        pb = prediction.pb
        if pb.HasField("struct_value"):
            embeddings.extend(list(pb.struct_value.fields["embeddings"].list_value.values[0].list_value.values))
    
    return [e.number_value for e in embeddings]