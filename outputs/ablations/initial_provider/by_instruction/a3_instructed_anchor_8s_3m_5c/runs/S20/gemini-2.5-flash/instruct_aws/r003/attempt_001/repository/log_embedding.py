import os
from google.cloud import aiplatform

def embed_log_message(log_message: str) -> list[float]:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Use the text-embedding-004 model
    model_name = "text-embedding-004"
    embeddings_model = aiplatform.private_preview.language_models.TextEmbeddingModel.from_pretrained(model_name)

    print(f"Embedding log message using Vertex AI's {model_name} model...")
    response = embeddings_model.predict([log_message])
    print("Embedding complete.")

    # The response contains a list of embeddings; we expect one for a single log message
    if response.embeddings:
        return response.embeddings[0].values
    else:
        return []
