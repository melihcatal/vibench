from speech_client import get_client, get_model


def poll_transcription(job_id: str):
    client = get_client()
    model = get_model()
    return client.audio.transcriptions.get(job_id, model=model)
