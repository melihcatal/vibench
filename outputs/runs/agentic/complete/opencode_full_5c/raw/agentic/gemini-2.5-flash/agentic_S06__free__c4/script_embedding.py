from speech_client import get_project_id, get_gcp_location
from speech_models import ScriptEmbeddingRequest
from google.cloud import aiplatform
from typing import List


def embed_script(text: str, model_name: str = "text-embedding-004") -> List[float]:
    project_id = get_project_id()
    location = get_gcp_location()

    # Initialize the PredictionServiceClient for the embedding model
    # The endpoint depends on the location. "aiplatform.init" doesn't provide a direct client for prediction.
    # Using aiplatform.gapic.PredictionServiceClient for direct access.

    # The endpoint for text-embedding-004 is specific to locations.
    # Example: us-central1-aiplatform.googleapis.com
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    endpoint = client.endpoint_path(
        project=project_id,
        location=location,
        publisher="google",
        model=model_name,  # Model family for embeddings
    )

    instances = aiplatform.gapic.FeatureValueList(
        values=[aiplatform.gapic.FeatureValue(string_value=text)]
    )

    # For the text-embedding-004 model, the instances format is typically a list of dictionaries with 'content' key.
    # Let's adjust the instance creation to match what the model expects.
    # The actual API for text-embedding-004 is simpler.
    # aiplatform.TextEmbeddingInput might be cleaner if we were using aiplatform.predict.PredictionServiceClient

    # Correct way to prepare instances for text-embedding-004 using gapic client
    # The instances should be a list of dicts or protobuf messages that the model understands.
    # For text-embedding-004, it expects `instances` as a list of dicts like `{"content": "your text"}`

    # Re-evaluating based on actual Vertex AI Embedding API usage:
    # The actual Vertex AI Python SDK for embeddings is `aiplatform.ImageGenerationModel.from_pretrained("text-embedding-004")`
    # or using `aiplatform.models.TextEmbeddingModel.from_pretrained()` which is simpler.

    # Let's use the higher-level SDK `aiplatform.models.TextEmbeddingModel`
    # Ensure `aiplatform.init` is called, which it is in `speech_client.py` and thus implied.

    # Re-doing this part to directly use the Embedding Model class for clarity and correctness with the SDK.
    # aiplatform.init is already called via get_vertex_ai_client for the project and location.

    embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    embeddings = embedding_model.get_embeddings([text])

    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return []
