from speech_client import get_client
from speech_models import TranscriptionRequest, normalize_transcription_response


def diarized_transcript(file_path: str, language: str | None = None):
    client = get_client()
    request = TranscriptionRequest(
        file_path=file_path,
        language=language,
        model="gpt-4o-transcribe",
        include=["word_timestamps"],
        diarize=True,
    )
    with open(request.file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=request.model,
            file=audio_file,
            language=request.language,
            response_format="verbose_json",
            timestamp_granularities=["word"],
            temperature=request.temperature,
        )
    result = normalize_transcription_response(response)
    return {"text": result.text, "raw": result.raw}
