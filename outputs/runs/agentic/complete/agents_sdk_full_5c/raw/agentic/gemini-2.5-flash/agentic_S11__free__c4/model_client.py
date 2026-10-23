import vertexai

def initialize_vertex_client(project_id: str, location: str):
    """Initializes the Google Cloud Vertex AI client.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for Vertex AI operations (e.g., 'us-central1').
    """
    vertexai.init(project=project_id, location=location)
    print(f"Vertex AI client initialized for project '{project_id}' in location '{location}'.")

def get_text_generation_model(model_id: str):
    """Returns a configured TextGenerationModel instance."
    from vertexai.preview.language_models import TextGenerationModel
    return TextGenerationModel.from_pretrained(model_id)
