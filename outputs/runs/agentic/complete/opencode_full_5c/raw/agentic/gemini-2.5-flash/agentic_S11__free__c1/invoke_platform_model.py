from google.cloud.aiplatform_v1.types import PredictRequest
from google.cloud.aiplatform_v1.types import Value
from model_client import get_prediction_client
from model_models import ModelInput, ModelOutput
import json


def invoke_vertex_ai_model(
    project_id: str, location: str, endpoint_id: str, model_input: ModelInput
) -> ModelOutput:
    client = get_prediction_client()
    endpoint_name = client.endpoint_path(
        project=project_id, location=location, endpoint=endpoint_id
    )

    instances = [json.loads(json.dumps({"prompt": model_input.text}))]

    # The format of each instance must conform to the schema required by the model deployed on the endpoint.
    # For text-bison@001, the instance format is {"prompt": "your prompt"}
    response = client.predict(endpoint=endpoint_name, instances=instances)

    predictions = response.predictions
    if predictions:
        # Assuming the model returns a dictionary with 'content'
        prediction_content = (
            predictions[0].get("content", "")
            if isinstance(predictions[0], dict)
            else str(predictions[0])
        )
        return ModelOutput(
            text=prediction_content,
            metadata={"deployed_model_id": response.deployed_model_id},
        )
    return ModelOutput(text="")
