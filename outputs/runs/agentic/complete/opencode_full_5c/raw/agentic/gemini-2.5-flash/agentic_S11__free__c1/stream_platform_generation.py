from google.cloud.aiplatform_v1.types import PredictRequest
from google.cloud.aiplatform_v1.types import Value
from model_client import get_prediction_client
from model_models import ModelInput
import json
from typing import Iterator


def stream_vertex_ai_generation(
    project_id: str, location: str, endpoint_id: str, model_input: ModelInput
) -> Iterator[str]:
    client = get_prediction_client()
    endpoint_name = client.endpoint_path(
        project=project_id, location=location, endpoint=endpoint_id
    )

    instances = [json.loads(json.dumps({"prompt": model_input.text}))]

    stream_response = client.stream_predict(endpoint=endpoint_name, instances=instances)

    for response in stream_response:
        predictions = response.predictions
        if predictions:
            prediction_content = (
                predictions[0].get("content", "")
                if isinstance(predictions[0], dict)
                else str(predictions[0])
            )
            yield prediction_content
