from google import genai



def get_model_client(config=None):
    config = config or {}
    return genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
