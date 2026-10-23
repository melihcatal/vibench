import os
from google.cloud import aiplatform

def ocr_embedding(text_segments, project_id=None, location="us-central1", model_name="text-embedding-004"):
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    aiplatform.init(project=project_id, location=location)

    embedding_model = aiplatform.language_models.TextEmbeddingModel.from_pretrained(model_name)
    
    embeddings_list = []
    if isinstance(text_segments, str):
        text_segments = [text_segments] # Ensure it's a list for batch prediction

    # The TextEmbeddingModel expects a list of texts
    predictions = embedding_model.predict(text_segments)

    for embedding in predictions.embeddings:
        embeddings_list.append(embedding.values)

    return {"embeddings": embeddings_list}
