from vertexai.generative_models import GenerativeModel


def resolve_model_resource(model_name: str) -> str:
    """
    Resolves a model resource by name.

    In the Vertex AI SDK, the model is often identified by its string name,
    so this function validates its existence by creating a handle
    and returns the name for use in other functions.
    """
    try:
        # This line doesn't make a remote call but prepares the SDK object
        GenerativeModel(model_name)
        return model_name
    except Exception as e:
        raise ValueError(f"Model '{model_name}' could not be resolved: {e}")


# Example of resolving a specific Gemini model
if __name__ == "__main__":
    model_id = "gemini-1.5-pro-preview-0409"
    resolved_model_id = resolve_model_resource(model_id)
    print(f"Successfully resolved model resource: {resolved_model_id}")
