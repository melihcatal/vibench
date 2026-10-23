from google.cloud import aiplatform
import os

def ocr_embedding(text_sections: list[str], config=None):
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GCP_PROJECT_ID"))
    location = config.get("location", os.environ.get("GCP_LOCATION", "us-central1"))
    
    aiplatform.init(project=project_id, location=location)
    
    # Using the 'text-embedding-004' model for embeddings
    model_name = "text-embedding-004"
    model = aiplatform.get_model_matching_pattern(display_name=model_name)
    
    # If the model is not found, you might need to enable the Vertex AI API and ensure the model is available in your region
    if not model:
        raise ValueError(f"Model '{model_name}' not found in project '{project_id}' and location '{location}'.")

    embeddings = []
    for text in text_sections:
        response = model.predict([text])
        embeddings.append(response.predictions[0]["embeddings"])

    return {"embeddings": embeddings}
