import os
from security_client import SecurityClient
from google.cloud.aiplatform_v1.types import PredictRequest


def embed_audit_note(text: str) -> list[float]:
    client = SecurityClient()

    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    # The endpoint for the public text-embedding-004 model
    endpoint = f"projects/{project_id}/locations/us-central1/publishers/google/models/text-embedding-004"

    instances = [{"content": text}]
    parameters = {}

    predict_request = PredictRequest(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    response = client.prediction_client.predict(request=predict_request)

    embeddings = []
    for prediction_val in response.predictions:
        # Assuming the embedding is directly in the prediction dictionary under 'embeddings' key
        # prediction_val is of type google.protobuf.struct_pb2.Value
        # Accessing the fields of the Value object for embeddings
        if "embeddings" in prediction_val.struct_value.fields:
            embedding_list = prediction_val.struct_value.fields[
                "embeddings"
            ].list_value.values
            embeddings.extend([field.number_value for field in embedding_list])

    return embeddings
