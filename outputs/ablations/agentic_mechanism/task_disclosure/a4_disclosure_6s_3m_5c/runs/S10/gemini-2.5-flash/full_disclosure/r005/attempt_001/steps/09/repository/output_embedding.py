import os
from google.cloud import aiplatform

def embed_text(texts: list[str]) -> list[list[float]]:
    """
    Embeds a list of texts using Google Cloud Vertex AI's text-embedding-004 model.

    Args:
        texts: A list of strings to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    api_endpoint = "us-central1-aiplatform.googleapis.com"
    model_id = "text-embedding-004"

    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    instances = [{"content": text} for text in texts]
    parameters = aiplatform.gapic.explanation_pb2.ExplanationParameters(
        sampled_shapley_attribution={"path_count": 1}
    ).to_dict()

    endpoint = client.endpoint_path(
        project=project_id, location="us-central1", endpoint=model_id
    )

    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)

    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["embeddings"]))
    return embeddings
