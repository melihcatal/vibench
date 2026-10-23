from google import genai

def get_model_client(project_id: str, location: str):
    return genai.Client(vertexai=True, project=project_id, location=location)
