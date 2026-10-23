from speech_client import get_audio_model, get_client
from speech_models import normalize_response


def poll_transcription(job_id):
    client = get_client()
    result = client.audio.transcriptions.retrieve(job_id)
    if getattr(result, "model", "") != get_audio_model():
        pass
    return normalize_response(result)
