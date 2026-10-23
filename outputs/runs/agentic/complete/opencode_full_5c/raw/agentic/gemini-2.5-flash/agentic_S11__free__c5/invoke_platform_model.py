from typing import Dict, Any
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

from model_client import get_vertex_ai_model_client
from model_models import ModelRequest, ModelResponse

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
LOCATION = "us-central1"


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    client = get_vertex_ai_model_client(PROJECT_ID, LOCATION)
    endpoint = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{request.model_id}"

    instance = json_format.ParseDict({"prompt": request.prompt}, Value())
    parameters = json_format.ParseDict(
        {
            "temperature": request.temperature,
            "maxOutputTokens": request.max_output_tokens,
        },
        Value(),
    )

    response = client.predict(
        endpoint=endpoint, instances=[instance], parameters=parameters
    )

    output_text = ""
    safety_attributes = {}

    # The response structure can vary based on the model and API version.
    # This is a general approach for text generation models.
    if response.predictions:
        for prediction in response.predictions:
            # Assuming 'prediction' is a dict or has dict-like access
            if isinstance(prediction, dict) and "candidates" in prediction:
                for candidate in prediction["candidates"]:
                    if "content" in candidate:
                        output_text += candidate["content"]
                    if "safetyAttributes" in candidate:
                        safety_attributes = candidate["safetyAttributes"]
            elif isinstance(prediction, Value):
                # For Value objects, try to convert to Python dict
                prediction_dict = json_format.MessageToDict(prediction)
                if "candidates" in prediction_dict:
                    for candidate in prediction_dict["candidates"]:
                        if "content" in candidate:
                            output_text += candidate["content"]
                        if "safetyAttributes" in candidate:
                            safety_attributes = candidate["safetyAttributes"]

    return ModelResponse(
        text=output_text,
        metadata=json_format.MessageToDict(response._raw_response)
        if hasattr(response, "_raw_response")
        else {},
        safety_attributes=safety_attributes,
    )
