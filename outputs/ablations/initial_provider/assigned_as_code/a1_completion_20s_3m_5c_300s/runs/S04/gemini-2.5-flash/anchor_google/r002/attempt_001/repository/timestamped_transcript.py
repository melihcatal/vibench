from google.cloud import speech_v1p1beta1 as speech
from speech_client import SpeechClientWrapper

def timestamped_transcript(payload, config=None):
    config = config or {}
    client_wrapper = SpeechClientWrapper()
    client = client_wrapper.get_client()

    audio_uri = payload["audio_uri"]
    language_code = payload["language_code"]

    recognition_config = speech.RecognitionConfig(
        language_code=language_code,
        enable_word_time_offsets=True,
    )

    audio = speech.RecognitionAudio(uri=audio_uri)

    operation = client.long_running_recognize(config=recognition_config, audio=audio)

    return {
        "job_id": operation.operation.name,
        "status": "SUBMITTED",
    }
