import os
from model_client import get_client
from vertexai.generative_models import GenerativeModel, Part

def get_model_by_name(model_name: str) -> GenerativeModel:
    """
    Resolves and returns a handle to a specific Vertex AI model resource.

    Args:
        model_name: The identifier of the model to resolve.

    Returns:
        A GenerativeModel instance representing the specified model.
    """
    get_client()

    # The model name itself is a provider-specific resource identifier
    print(f"Resolving model resource for: {model_name}")
    model = GenerativeModel(model_name)
    
    # Verifying the model handle by making a small call
    try:
        model.generate_content("hello", generation_config={"max_output_tokens": 1})
        print(f"Successfully resolved and verified model: {model_name}")
    except Exception as e:
        print(f"Failed to resolve or verify model {model_name}: {e}")
        raise
        
    return model

def select_default_model() -> GenerativeModel:
    """
    Selects the default model specified in an environment variable.
    """
    # Using a provider-specific model name like 'gemini-1.0-pro'
    default_model_name = os.getenv("VERTEX_AI_MODEL_ID", "gemini-1.0-pro")
    return get_model_by_name(default_model_name)

