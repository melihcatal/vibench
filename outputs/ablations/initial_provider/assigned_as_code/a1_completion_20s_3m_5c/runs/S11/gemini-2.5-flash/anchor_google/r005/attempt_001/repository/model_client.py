from google.cloud import aiplatform

def get_vertex_ai_client(project_id: str, location: str):
    return aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})

def get_gemini_model_id(project_id: str, location: str, model_name: str = "gemini-2.5-flash"):
    # In a real scenario, this might involve looking up a deployed model ID or version.
    # For now, we'll just return the base model name used by the genai client.
    return model_name
