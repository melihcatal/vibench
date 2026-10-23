from google.cloud import aiplatform

from observability_client import build_client


def incident_summary(payload, config=None):
    _, config = build_client(config)
    text = payload.get("findings", "")
    return {"summary": text[:280], "provider": "google-cloud-aiplatform", "project_id": config["project_id"]}
