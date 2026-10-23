import os
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
import json
from typing import Dict, Any, List, Iterator


class VertexAIModelClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=project_id, location=location)
        self.prediction_client = aiplatform.gapic.PredictionServiceClient(
            client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
        )

    def _predict(
        self,
        model_name: str,
        instances: List[Dict[str, Any]],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{model_name}"

        # The AI Platform Prediction API can't take requests directly as JSON.
        # It needs to be a list of instances, where each instance is a
        # `google.protobuf.Value` object.
        instances_proto = [
            json_format.ParseDict(instance, predict.Instance()._pb)
            for instance in instances
        ]
        parameters_proto = json_format.ParseDict(parameters, predict.Parameters()._pb)

        response = self.prediction_client.predict(
            endpoint=endpoint,
            instances=instances_proto,
            parameters=parameters_proto,
        )

        # The API returns a list of predictions, where each prediction is a
        # `google.protobuf.Value` object.
        # We need to convert them back to Python dictionaries.
        predictions = [
            json_format.MessageToDict(prediction) for prediction in response.predictions
        ]
        return {"predictions": predictions}

    def generate_content(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
    ) -> str:
        instances = [{"prompt": prompt}]
        parameters = {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
            "topP": 0.95,
            "topK": 40,
        }

        response = self._predict(
            model_name=model_name, instances=instances, parameters=parameters
        )

        if response and response["predictions"]:
            return response["predictions"][0]["content"]
        return ""

    def stream_generate_content(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
    ) -> Iterator[str]:
        # Vertex AI SDK for streaming is a bit different. I'll use the higher-level client.
        model = aiplatform.GenerativeModel(model_name)

        # The prompt can be a string or a list of parts for multi-modal.
        # For text generation, a string is fine.
        generation_config = {
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 40,
        }

        responses = model.generate_content(
            contents=prompt, generation_config=generation_config, stream=True
        )

        for response in responses:
            yield response.text


# Environment variables for configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

vertex_client = VertexAIModelClient(project_id=PROJECT_ID, location=LOCATION)
