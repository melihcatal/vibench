from google import genai

def get_genai_client(project_id: str, location: str):
    return genai.Client(vertexai=True, project=project_id, location=location)

def get_default_model_id():
    return "gemini-2.5-flash"
