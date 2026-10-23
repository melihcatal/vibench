import vertexai

def select_model_resource(project_id: str, location: str, model_id: str):
    """Resolves a Vertex AI model resource."""
    vertexai.init(project=project_id, location=location)
    # In Vertex AI, getting a model usually means getting an instance of the model class
    # For generative models, it's often by instantiating GenerativeModel with the ID
    # This function demonstrates a conceptual selection.
    try:
        model_resource = vertexai.preview.generative_models.GenerativeModel(model_id)
        print(f"Selected model resource: {model_id}")
        return model_resource
    except Exception as e:
        print(f"Error selecting model resource {model_id}: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    # model = select_model_resource("your-gcp-project-id", "us-central1", "gemini-pro")
    # if model:
    #     print(f"Model object type: {type(model)}")
    pass
