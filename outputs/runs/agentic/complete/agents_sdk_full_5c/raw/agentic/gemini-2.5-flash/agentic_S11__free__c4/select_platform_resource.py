import vertexai

def select_platform_resource(project_id: str, location: str, preferred_model_id: str) -> str:
    """Resolves a specific Google Cloud Vertex AI model resource ID."""
    # In a real scenario, this might involve more complex logic like checking model availability
    # or selecting based on performance metrics. For this example, we simply return the preferred ID.
    vertexai.init(project=project_id, location=location)
    # A more advanced implementation might list models to verify existence:
    # from vertexai.language_models import TextGenerationModel
    # models = TextGenerationModel.list_models()
    # if preferred_model_id not in [m.name for m in models]:
    #     raise ValueError(f"Model {preferred_model_id} not found.")
    return preferred_model_id
