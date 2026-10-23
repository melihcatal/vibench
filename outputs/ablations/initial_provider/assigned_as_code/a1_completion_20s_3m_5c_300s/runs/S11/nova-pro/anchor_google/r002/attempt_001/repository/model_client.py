from google import genai

def get_client(config):
    return genai.Client(vertexai=True, project=config["project_id"], location=config["location"])