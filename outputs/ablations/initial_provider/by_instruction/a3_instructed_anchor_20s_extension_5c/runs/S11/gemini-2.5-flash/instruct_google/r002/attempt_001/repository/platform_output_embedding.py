from google.cloud import aiplatform

def platform_output_embedding(project_id: str, location: str, text_content: str):
    """Embeds platform outputs for evaluation or retrieval using Google Cloud Vertex AI."""
    aiplatform.init(project=project_id, location=location)

    # The text embedding model from Vertex AI
    # Model ID for text-embedding-004 is often used for embeddings.
    # Check the latest available models in the Vertex AI documentation.
    model_id = "text-embedding-004" # or other appropriate embedding model

    try:
        model = aiplatform.Model.create(model_id=model_id)
        instances = [{ "content": text_content }]
        response = model.predict(instances=instances)
        
        # The embedding is typically in the predictions list
        embeddings = response.predictions[0]["embeddings"] if response.predictions else []
        
        return {"embeddings": embeddings}

    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return {"embeddings": [], "error": str(e), "note": "Embedding generation failed."}
