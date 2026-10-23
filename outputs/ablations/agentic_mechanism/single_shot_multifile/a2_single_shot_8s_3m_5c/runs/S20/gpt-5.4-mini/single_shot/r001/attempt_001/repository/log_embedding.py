from google.cloud import aiplatform
import os


if __name__ == "__main__":
    text = os.getenv("LOG_TEXT", "")
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")
    location = os.getenv("VERTEX_LOCATION", "us-central1")
    model_name = os.getenv("VERTEX_EMBEDDING_MODEL", "text-embedding-004")
    if not project:
        raise ValueError("Missing Google Cloud project id")
    aiplatform.init(project=project, location=location)
    print({"model": model_name, "text": text, "embedding_ready": True if text else False})
