import os
from model_client import get_vertex_ai_model_client
from typing import Dict, Any, List

def embed_text(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION")
    # Using a specific embedding model ID for Vertex AI
    embedding_model_id = config.get("embedding_model_id") or "text-embedding-004"

    vertex_ai = get_vertex_ai_model_client(project_id, location)

    texts_to_embed = payload.get("texts", [])
    if not isinstance(texts_to_embed, list):
        texts_to_embed = [texts_to_embed]

    # Initialize the embedding model from Vertex AI
    # The TextEmbeddingModel is part of aiplatform.models
    # It's possible that the embedding model is accessed slightly differently, e.g., via a PredictionServiceClient
    # For the purpose of this exercise, I'll assume a direct model loading approach through aiplatform
    
    # As per Vertex AI documentation, embedding models are usually called via PredictionServiceClient
    # or using a dedicated TextEmbeddingModel class if available in the SDK preview.
    # Let's use the GenerativeModel approach for consistency with previous files, assuming it can handle embeddings
    # However, the more direct approach for embeddings is typically:
    # from google.cloud.aiplatform.private_preview import TextEmbeddingModel
    # model = TextEmbeddingModel.from_pretrained(embedding_model_id)
    # embeddings = model.batch_embed_text(texts_to_embed)

    # Sticking to the GenerativeModel if it supports embeddings, which is not typical for pure embeddings
    # Let's adjust to use the correct embedding client for Vertex AI
    from google.cloud.aiplatform import gapic
    
    # Create a client for the Prediction Service
    # The endpoint for embedding models is typically different from generative models
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    prediction_client = gapic.PredictionServiceClient(client_options=client_options)

    instances = [{
        "prompt": text,
        "task_type": "RETRIEVAL_QUERY" # Example task type, adjust as needed
    } for text in texts_to_embed]

    # The endpoint for embedding models is typically in the format:
    # projects/<PROJECT_ID>/locations/<LOCATION>/publishers/google/models/<MODEL_ID>
    endpoint = prediction_client.model_path(project_id, location, "google", embedding_model_id)

    # The predict method is used for embedding models
    response = prediction_client.predict(endpoint=endpoint, instances=instances)

    # Extract embeddings from the response
    embeddings = []
    for prediction in response.predictions:
        # Assuming each prediction has an 'embedding' field which is a list of floats
        if "embeddings" in prediction and "values" in prediction["embeddings"]:
            embeddings.append(prediction["embeddings"]["values"])
        
    return {"embeddings": embeddings}
