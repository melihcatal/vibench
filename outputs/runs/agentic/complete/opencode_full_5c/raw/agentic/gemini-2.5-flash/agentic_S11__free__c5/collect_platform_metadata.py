from typing import Dict, Any
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

from model_client import get_vertex_ai_model_client
from model_models import ModelRequest, ModelResponse

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
LOCATION = "us-central1"


def collect_platform_metadata(request: ModelRequest) -> ModelResponse:
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
    if response.predictions:
        for prediction in response.predictions:
            if isinstance(prediction, dict) and "candidates" in prediction:
                for candidate in prediction["candidates"]:
                    if "content" in candidate:
                        output_text += candidate["content"]
                    if "safetyAttributes" in candidate:
                        safety_attributes = candidate["safetyAttributes"]
            elif isinstance(prediction, Value):
                prediction_dict = json_format.MessageToDict(prediction)
                if "candidates" in prediction_dict:
                    for candidate in prediction_dict["candidates"]:
                        if "content" in candidate:
                            output_text += candidate["content"]
                        if "safetyAttributes" in candidate:
                            safety_attributes = candidate["safetyAttributes"]

    # Extracting metadata from the response object
    metadata = {
        "model_id": request.model_id,
        "project_id": PROJECT_ID,
        "location": LOCATION,
        "raw_response": json_format.MessageToDict(response._raw_response)
        if hasattr(response, "_raw_response")
        else {},
        # Add more specific metadata like usage, resource IDs if available in the response
        # For Vertex AI's predict, detailed usage often comes in the response headers or a specific field
        # which might require deeper inspection or parsing.
        # For now, we'll include the raw response which contains a lot of info.
    }

    return ModelResponse(
        text=output_text, metadata=metadata, safety_attributes=safety_attributes
    )
