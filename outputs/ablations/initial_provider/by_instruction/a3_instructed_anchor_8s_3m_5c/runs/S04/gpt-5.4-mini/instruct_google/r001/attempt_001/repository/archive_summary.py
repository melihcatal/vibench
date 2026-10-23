from google.cloud import aiplatform


def archive_summary(transcript: str):
    aiplatform.init()
    return {"summary": transcript[:280], "provider": "google-cloud-aiplatform"}
