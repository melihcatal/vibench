from google.cloud import aiplatform

def embed_audit_notes(project_id: str, location: str, text: str):
    """Embeds secret audit notes using Google Cloud Vertex AI's embedding model.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where the model is deployed (e.g., "us-central1").
        text: The secret audit notes to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.get_model_garden_models(model_id="text-embedding-004")
    embeddings = model.predict([text])
    return embeddings.predictions[0].values

if __name__ == '__main__':
    # Example usage (replace with your actual project ID and location)
    project_id = "your-gcp-project-id"
    location = "us-central1"
    audit_notes = "This secret was last rotated 90 days ago. It is used by the authentication service."
    
    try:
        embedding = embed_audit_notes(project_id, location, audit_notes)
        print(f"Embedding for '{audit_notes}': {embedding[:5]}...") # Print first 5 elements
    except Exception as e:
        print(f"An error occurred: {e}")
