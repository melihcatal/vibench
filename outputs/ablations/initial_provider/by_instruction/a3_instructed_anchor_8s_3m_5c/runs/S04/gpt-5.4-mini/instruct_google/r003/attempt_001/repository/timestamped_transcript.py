from typing import Any, Dict

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_google_speech_config


def request_timestamped_transcript(gcs_uri: str, language_code: str = "en-US") -> Dict[str, Any]:
    client = speech.SpeechClient()
    request = {
        "config": build_google_speech_config({
            "language_code": language_code,
            "enable_word_time_offsets": True,
        }),
        "audio": {"uri": gcs_uri},
    }
    operation = client.long_running_recognize(request=request)
    return {"job_name": operation.operation.name, "provider": "google", "timestamps": True}
