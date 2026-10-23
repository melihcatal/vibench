from google.cloud import speech



def diarized_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    operation = client.long_running_recognize(
        config=speech.RecognitionConfig(
            language_code=payload["language_code"],
            enable_speaker_diarization=True,
        ),
        audio=speech.RecognitionAudio(uri=payload["audio_uri"]),
    )
    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED",
    }