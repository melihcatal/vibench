import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def get_embedding(text_content: str, config: dict = None) -> Dict[str, Any]:
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("location") or "us-central1"

    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")

    aiplatform.init(project=project_id, location=location)

    # The embedding model to use. Text embeddings are available under the `textembedding-gecko` family.
    # The specific model ID might vary, so using a common one here.
    # For the latest model IDs, refer to Vertex AI documentation.
    model_name = "textembedding-gecko@003"

    # Initialize the TextEmbeddingModel
    model = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    ).get_model_full_name(project=project_id, location=location, model=model_name)

    # Prepare the instance for embedding
    instances = aiplatform.gapic.accelerator_type.EmbeddingData(
        text=text_content
    ).to_json()

    # In a real scenario, you would create a list of instances for batch prediction.
    # For a single text, we still wrap it in a list.
    instances_list = [instances]

    # Predict embeddings
    try:
        response = aiplatform.gapic.PredictionServiceClient(
            client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
        ).predict(
            endpoint=f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}",
            instances=instances_list,
        )

        # Parse the response to get the embedding vector
        embeddings = []
        for prediction in response.predictions:
            # The embedding is typically nested in a structure like this based on the model output format
            if "embeddings" in prediction and "values" in prediction["embeddings"]:
                embeddings.append(list(prediction["embeddings"]["values"]))
            elif "embedding" in prediction and "values" in prediction["embedding"]:
                 embeddings.append(list(prediction["embedding"]["values"]))
            else: # Fallback for unexpected structure or direct value
                embeddings.append(list(prediction))

        return {"embedding": embeddings[0] if embeddings else []}

    except Exception as e:
        # Handle cases where the model response structure is different or an error occurs
        print(f"Error getting embedding: {e}")
        return {"embedding": []}
