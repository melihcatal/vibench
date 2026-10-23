from speech_client import get_audio_model, get_client
from speech_models import normalize_response


def diarized_transcript(file_path, prompt="", language="en"):
    client = get_client()
    with open(file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=get_audio_model(),
            file=audio_file,
            prompt=prompt or None,
            language=language or None,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            extra_body={"diarize": True},
        )
    return normalize_response(result)
