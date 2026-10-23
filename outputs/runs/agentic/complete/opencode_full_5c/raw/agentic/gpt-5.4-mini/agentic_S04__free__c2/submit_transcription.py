from speech_client import get_audio_model, get_client
from speech_models import TranscriptionRequest, normalize_response


def submit_transcription(file_path, prompt="", language=""):
    client = get_client()
    request = TranscriptionRequest(
        file_path=file_path, prompt=prompt, language=language
    )
    with open(request.file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=get_audio_model(),
            file=audio_file,
            prompt=request.prompt or None,
            language=request.language or None,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
    return normalize_response(result)
