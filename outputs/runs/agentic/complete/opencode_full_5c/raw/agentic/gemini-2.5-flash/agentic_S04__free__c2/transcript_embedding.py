import os
from typing import List
from google.cloud import aiplatform


def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    # Initialize Vertex AI
    # aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_LOCATION")) # Replace with your project and location

    # For simplicity, assuming project and location are set up or default

    model_name = "text-embedding-gecko@001"  # Concrete model identifier

    # The client library automatically handles authentication if you have gcloud configured
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )  # Example endpoint, adjust as needed

    instances = [{"content": segment} for segment in segments]
    parameters = aiplatform.gapic.PredictRequest.FlattenedStruct(value={})

    # Construct the endpoint path
    # project_id = os.environ.get("GCP_PROJECT_ID")
    # location = os.environ.get("GCP_LOCATION")
    # endpoint = f"projects/{project_id}/locations/{location}/endpoints/{model_name}"
    # For simplicity, using a hardcoded example path. User needs to replace project_id and location
    endpoint = f"projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/{model_name}"

    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["embeddings"]["values"]))

    return embeddings
