from google.cloud.aiplatform_v1.types import PredictRequest
from google.cloud.aiplatform_v1.types import Value
from model_client import get_prediction_client
from model_models import ModelInput, ModelOutput
import json


def collect_vertex_ai_metadata(
    project_id: str, location: str, endpoint_id: str, model_input: ModelInput
) -> ModelOutput:
    client = get_prediction_client()
    endpoint_name = client.endpoint_path(
        project=project_id, location=location, endpoint=endpoint_id
    )

    instances = [json.loads(json.dumps({"prompt": model_input.text}))]

    response = client.predict(endpoint=endpoint_name, instances=instances)

    metadata = {
        "deployed_model_id": response.deployed_model_id,
        "model_resource_name": response.model,
        "model_version_id": response.model_version_id,
        "explanation_metadata": response.explanation_metadata,
        "explanation_outputs": response.explanation_outputs,
    }

    predictions = response.predictions
    if predictions:
        prediction_content = (
            predictions[0].get("content", "")
            if isinstance(predictions[0], dict)
            else str(predictions[0])
        )
        return ModelOutput(text=prediction_content, metadata=metadata)
    return ModelOutput(text="", metadata=metadata)
