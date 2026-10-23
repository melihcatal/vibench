
import os
from google.cloud import aiplatform_v1beta1 as aiplatform
from google.api_core.client_options import ClientOptions


class EmbeddingsClient:
    def __init__(self, project_id: str, location: str, api_endpoint: str = "us-central1-aiplatform.googleapis.com"):
        self.project_id = project_id
        self.location = location
        self.api_endpoint = api_endpoint
        client_options = ClientOptions(api_endpoint=self.api_endpoint)
        self.client = aiplatform.PredictionServiceClient(client_options=client_options)

    def get_embedding(self, text: str, model_name: str = "text-embedding-004") -> list[float]:
        endpoint = self.client.endpoint_path(
            project=self.project_id, location=self.location, endpoint="locations/us-central1/endpoints/2397022026850236416"
        )
        instance = aiplatform.Tensor(
            struct_value={
                "text": text,
                "task_type": "SEMANTIC_SIMILARITY",
                "title": "",
                "query/document": "DOCUMENT"
            }
        )
        instances = [instance]
        parameters = aiplatform.Tensor(
            struct_value={
                "model_name": model_name
            }
        )
        response = self.client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
        return response.predictions[0].struct_value["embeddings"].list_value[0]
