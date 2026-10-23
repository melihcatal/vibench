from google.cloud import aiplatform_v1 as aiplatform
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
EMBEDDING_MODEL_NAME = "text-embedding-004" # Or text-embedding-preview-0409

def get_embeddings_client():
    """Initializes and returns a Vertex AI Prediction Service client."""
    client_options = {"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
    return aiplatform.PredictionServiceClient(client_options=client_options)

def embed_text_with_client(texts: list[str]) -> list[list[float]]:
    """Generates embeddings for a list of texts using the Vertex AI Embeddings API.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    client = get_embeddings_client()
    endpoint = client.endpoint_path(
        project=PROJECT_ID, location=LOCATION, publisher="google", model=EMBEDDING_MODEL_NAME
    )
    instances = [{"content": text} for text in texts]
    
    predict_request = aiplatform.PredictRequest(
        endpoint=endpoint, instances=instances
    )
    response = client.predict(predict_request)
    
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["embeddings"]["values"]))
    return embeddings
