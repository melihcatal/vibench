from google.cloud.speech_v2.types import cloud_speech

def normalize_partial_result(result):
    return " ".join([alternative.transcript for alternative in result.alternatives])

def normalize_final_result(result):
    return " ".join([alternative.transcript for alternative in result.alternatives])

def create_recognition_request(audio_bytes, language_code="en-US"):
    return {
        "config": {
            "encoding": "LINEAR16",
            "sample_rate_hertz": 16000,
            "language_code": language_code,
            "model": "latest_long",
        },
        "audio": {"content": audio_bytes},
    }