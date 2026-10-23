from google.cloud import aiplatform

from storage_client import storage_client


def stored_asset_summary(payload, config=None):
    _, config = storage_client(config)
    aiplatform.init(project=config["project_id"], location=config.get("location", "us-central1"))
    model = aiplatform.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(payload["text"])
    return {"summary": response.text}
