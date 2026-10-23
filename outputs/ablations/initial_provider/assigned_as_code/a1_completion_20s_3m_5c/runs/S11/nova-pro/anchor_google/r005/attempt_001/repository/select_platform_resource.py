from google import genai



def select_platform_resource(model_name, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        model = client.models.get(model_name)
    return model