from google.cloud import aiplatform
from google.protobuf import json_format
from google.cloud.aiplatform.gapic.schema import predict_v1_types
from document_client import get_vertex_ai_prediction_client
import os


def extract_structured_fields(text: str, model_id: str) -> dict:
    client = get_vertex_ai_prediction_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    # The endpoint for a custom Vertex AI model
    endpoint = client.endpoint_path(
        project=project_id, location=location, endpoint=model_id
    )

    instance = predict_v1_types.Instance(struct_value={"text_content": text})._pb  # type: ignore
    instances = [instance]

    response = client.predict(endpoint=endpoint, instances=instances)

    extracted_fields = {}
    for prediction in response.predictions:
        # Assuming the prediction is a struct that contains the extracted fields
        if (
            "extracted_data" in prediction
        ):  # Example key, adjust based on your model output
            extracted_fields = prediction["extracted_data"]
            break
        elif isinstance(prediction, dict):
            # If the prediction is a dictionary directly, use it
            extracted_fields = prediction
            break

    return extracted_fields
