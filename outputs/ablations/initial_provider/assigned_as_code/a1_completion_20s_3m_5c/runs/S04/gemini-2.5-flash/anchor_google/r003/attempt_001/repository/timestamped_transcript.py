from google.cloud import speech

def timestamped_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()

    recognition_config = speech.RecognitionConfig(
        language_code=payload["language_code"],
        enable_word_time_offsets=True,
    )

    audio = speech.RecognitionAudio(uri=payload["audio_uri"])

    operation = client.long_running_recognize(
        config=recognition_config,
        audio=audio,
    )
    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED_TIMESTAMPED",
    }
