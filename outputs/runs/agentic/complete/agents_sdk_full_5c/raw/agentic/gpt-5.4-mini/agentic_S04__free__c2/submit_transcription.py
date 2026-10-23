from speech_client import get_client
from speech_models import TranscriptionRequest, normalize_transcription_response


def submit_transcription(file_path: str, language: str | None = None, prompt: str | None = None):
    client = get_client()
    request = TranscriptionRequest(file_path=file_path, language=language, prompt=prompt)
    with open(request.file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=request.model,
            file=audio_file,
            language=request.language,
            prompt=request.prompt,
            response_format=request.response_format,
            temperature=request.temperature,
        )
    return normalize_transcription_response(response)
