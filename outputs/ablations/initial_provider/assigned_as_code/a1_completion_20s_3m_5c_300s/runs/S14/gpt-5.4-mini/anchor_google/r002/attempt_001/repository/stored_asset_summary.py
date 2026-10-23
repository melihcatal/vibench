import vertexai
from vertexai.generative_models import GenerativeModel


def stored_asset_summary(payload, config=None):
    config = config or {}
    vertexai.init(project=config["project_id"], location=config.get("location", "us-central1"))
    model = GenerativeModel(config.get("model_id", "gemini-1.5-pro"))
    response = model.generate_content(payload["text"])
    return {"summary": response.text}
