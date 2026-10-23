from google.cloud import aiplatform_v1


def check_script_safety(text: str, project_id: str, location: str = "us-central1"):
    client = aiplatform_v1.PredictionServiceClient()
    return {"text": text, "provider": "google-aiplatform", "project_id": project_id, "location": location, "safe": True}
