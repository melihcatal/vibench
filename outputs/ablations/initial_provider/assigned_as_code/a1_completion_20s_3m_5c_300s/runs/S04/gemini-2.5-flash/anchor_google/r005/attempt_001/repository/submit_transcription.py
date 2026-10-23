from google.cloud import speech


def submit_transcription(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(language_code=payload["language_code"]),
        audio=speech.RecognitionAudio(uri=payload["audio_uri"]),
    )
    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED",
    }
