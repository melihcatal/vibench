from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

def invoke_model(project_id: str, location: str, model_id: str, prompt: str):
    """Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client."""

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        display_name="text-bison-endpoint",
        project=project_id,
        location=location,
        model_id=model_id # This should be the deployed model ID, e.g., "text-bison@001"
    )

    instances = [
        json_format.ParseDict(
            {"prompt": prompt}, Value()
        ),
    ]

    parameters = json_format.ParseDict(
        {"temperature": 0.2, "maxOutputTokens": 256, "topP": 0.95, "topK": 40}, Value()
    )

    response = endpoint.predict(instances=instances, parameters=parameters)

    return response.predictions[0]
