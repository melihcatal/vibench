from google.cloud import speech_v1p1beta1 as speech
from speech_client import SpeechClientWrapper

def diarized_transcript(payload, config=None):
    config = config or {}
    client_wrapper = SpeechClientWrapper()
    client = client_wrapper.get_client()

    audio_uri = payload["audio_uri"]
    language_code = payload["language_code"]
    speaker_count = payload.get("speaker_count", 2) # Default to 2 speakers

    recognition_config = speech.RecognitionConfig(
        language_code=language_code,
        enable_speaker_diarization=True,
        diarization_speaker_count=speaker_count,
        model="default", # Use default model for diarization
    )

    audio = speech.RecognitionAudio(uri=audio_uri)

    operation = client.long_running_recognize(config=recognition_config, audio=audio)

    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED",
    }
