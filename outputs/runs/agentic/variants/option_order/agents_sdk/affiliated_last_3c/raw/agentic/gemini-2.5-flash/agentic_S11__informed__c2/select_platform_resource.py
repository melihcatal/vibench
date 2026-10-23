import vertexai

def select_vertex_ai_model_resource(project_id: str, location: str, model_name: str):
    vertexai.init(project=project_id, location=location)
    # In Vertex AI, selecting a 'resource' is often just knowing the model name.
    # The GenerativeModel class itself acts as a resource handle.
    # This function primarily validates access or returns the model name for consistency.
    available_models = vertexai.get_available_models()
    if model_name not in available_models:
        raise ValueError(f"Model {model_name} not available in {location}.")
    return model_name
