from google import genai


def select_platform_resource(config):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    model = client.models.get(model="gemini-2.5-flash")
    return model.name