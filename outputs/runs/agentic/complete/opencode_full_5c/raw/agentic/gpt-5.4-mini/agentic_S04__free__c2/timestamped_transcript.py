from speech_client import get_audio_model, get_client
from speech_models import normalize_response


def timestamped_transcript(file_path, granularity="word"):
    client = get_client()
    with open(file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=get_audio_model(),
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=[granularity],
        )
    return normalize_response(result)
