import vertexai
from vertexai.generative_models import GenerativeModel


def invoke_platform_model(payload, config=None):
    config = config or {}
    vertexai.init(project=config["project_id"], location=config["location"])
    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(payload["text"])
    return {"text": response.text or ""}
