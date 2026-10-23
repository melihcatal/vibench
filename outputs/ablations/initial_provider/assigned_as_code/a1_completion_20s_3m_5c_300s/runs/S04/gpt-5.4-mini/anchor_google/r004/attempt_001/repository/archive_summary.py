from google.cloud import speech


def archive_summary(payload, config=None):
    client = speech.SpeechClient()
    operation_name = payload["job_id"]
    return {"job_id": operation_name, "summary": payload.get("summary", "")}
