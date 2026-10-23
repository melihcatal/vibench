from google.cloud import aiplatform
import os

def get_text_embedding(text: str, project_id: str, location: str = "us-central1") -> list:
    aiplatform.init(project=project_id, location=location)

    # The model_id can vary, using a common one for text embeddings
    # Refer to Google Cloud Vertex AI documentation for available models and their IDs
    model_id = "textembedding-gecko@001"

    # Instantiate the TextEmbeddingModel
    model = aiplatform.gapic.PredictionServiceClient(client_options={
        "api_endpoint": f"{location}-aiplatform.googleapis.com"
    })

    instance = {"content": text}
    instances = [instance]

    # The endpoint ID is typically derived from the model ID
    endpoint_id = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    response = model.predict(endpoint=endpoint_id, instances=instances)

    embeddings = []
    for prediction in response.predictions:
        # Assuming the embedding is directly accessible in the prediction dictionary
        if "embeddings" in prediction and "values" in prediction["embeddings"]:
            embeddings.append(prediction["embeddings"]["values"])
    return embeddings[0] if embeddings else []
