from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict_v1_types
from document_client import get_vertex_ai_prediction_client
import os


def check_content_safety(text: str) -> dict:
    client = get_vertex_ai_prediction_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    publisher = "google"
    model_name = "text-bison"  # Example pre-trained model for text generation with safety attributes

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    endpoint = client.endpoint_path(
        project=project_id, location=location, publisher=publisher, model=model_name
    )

    instance = predict_v1_types.Instance(struct_value={"prompt": text})._pb  # type: ignore
    instances = [instance]

    response = client.predict(endpoint=endpoint, instances=instances)

    safety_attributes = {}
    for prediction in response.predictions:
        if "safetyAttributes" in prediction:
            safety_attributes = prediction["safetyAttributes"]
            break  # Assuming first prediction has safety attributes

    return safety_attributes
