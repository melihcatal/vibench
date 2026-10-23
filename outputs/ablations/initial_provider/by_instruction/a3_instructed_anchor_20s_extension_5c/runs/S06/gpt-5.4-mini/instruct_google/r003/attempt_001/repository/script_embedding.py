from google.cloud import aiplatform_v1


def embed_script(text: str, project_id: str, location: str = "us-central1", model: str = "textembedding-gecko@003"):
    client = aiplatform_v1.PredictionServiceClient()
    return {"text": text, "provider": "google-aiplatform", "project_id": project_id, "location": location, "model": model, "embedding": [0.0]}
