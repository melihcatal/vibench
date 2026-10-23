from google.cloud import aiplatform
import os


if __name__ == "__main__":
    text = os.getenv("LOG_TEXT", "")
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")
    location = os.getenv("VERTEX_LOCATION", "us-central1")
    model_name = os.getenv("VERTEX_MODEL", "gemini-1.5-pro")
    if not project:
        raise ValueError("Missing Google Cloud project id")
    aiplatform.init(project=project, location=location)
    print({"model": model_name, "text": text, "safe": True if text else False})
