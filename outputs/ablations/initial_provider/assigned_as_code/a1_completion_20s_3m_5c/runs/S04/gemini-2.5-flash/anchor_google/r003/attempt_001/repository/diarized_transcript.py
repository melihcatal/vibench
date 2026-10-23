from google.cloud import speech

def diarized_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    
    recognition_config = speech.RecognitionConfig(
        language_code=payload["language_code"],
        enable_speaker_diarization=True,
        diarization_speaker_count=payload.get("speaker_count"),
        # model="video", # A model that supports diarization
    )

    audio = speech.RecognitionAudio(uri=payload["audio_uri"])

    operation = client.long_running_recognize(
        config=recognition_config,
        audio=audio,
    )
    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED_DIARIZATION",
    }
