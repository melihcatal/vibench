import vertexai
from model_client import GCP_PROJECT_ID, GCP_LOCATION

def find_gemini_model():
    """
    Finds and returns a reference to a Gemini model in Google Cloud Vertex AI.
    """
    if not GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)

    # List all models and find one with 'gemini' in its name
    # This demonstrates resolving a specific resource from a provider's list
    available_models = vertexai.Model.list()
    for model in available_models:
        # Provider-identifying signal in model name format
        if "gemini" in model.name:
            return model # Returns the vertexai.Model object
    
    return None
