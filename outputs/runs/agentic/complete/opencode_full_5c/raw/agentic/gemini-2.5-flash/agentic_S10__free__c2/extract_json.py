from model_client import VertexAIModelClient
from model_models import JsonExtractionRequest, JsonExtractionResponse


def extract_json(request: JsonExtractionRequest) -> JsonExtractionResponse:
    client = VertexAIModelClient()
    return client.extract_json(request)
