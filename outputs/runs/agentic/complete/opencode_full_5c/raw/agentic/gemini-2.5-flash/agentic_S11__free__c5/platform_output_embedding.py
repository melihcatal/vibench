from typing import List
from google.cloud import aiplatform
from google.protobuf.struct_pb2 import Value
from google.protobuf import json_format

from model_client import get_vertex_ai_model_client
from model_models import ModelResponse

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"
LOCATION = "us-central1"
EMBEDDING_MODEL_ID = "text-embedding-004"


def platform_output_embedding(response: ModelResponse) -> ModelResponse:
    """
    Embeds platform outputs for evaluation or retrieval using Vertex AI's embedding model.
    """
    client = get_vertex_ai_model_client(PROJECT_ID, LOCATION)
    endpoint = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{EMBEDDING_MODEL_ID}"

    instance = json_format.ParseDict({"text": response.text}, Value())

    # The embedding model typically uses the 'predict' method.
    predict_response = client.predict(endpoint=endpoint, instances=[instance])

    embeddings: List[float] = []
    if predict_response.predictions:
        # Assuming the structure has a 'embeddings' key within each prediction
        for prediction in predict_response.predictions:
            if isinstance(prediction, dict) and "embeddings" in prediction:
                embeddings = prediction["embeddings"]
                break
            elif isinstance(prediction, Value):
                prediction_dict = json_format.MessageToDict(prediction)
                if "embeddings" in prediction_dict:
                    embeddings = prediction_dict["embeddings"]
                    break

    response.embedding = embeddings
    return response
