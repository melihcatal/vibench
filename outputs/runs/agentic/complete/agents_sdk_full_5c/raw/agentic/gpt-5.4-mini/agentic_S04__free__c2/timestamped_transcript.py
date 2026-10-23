from speech_client import get_client
from speech_models import TranscriptionRequest, normalize_transcription_response


def timestamped_transcript(file_path: str, granularity: str = "word"):
    client = get_client()
    request = TranscriptionRequest(
        file_path=file_path,
        model="gpt-4o-transcribe",
        response_format="verbose_json",
        timestamp_granularities=[granularity],
    )
    with open(request.file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=request.model,
            file=audio_file,
            response_format=request.response_format,
            timestamp_granularities=request.timestamp_granularities,
        )
    result = normalize_transcription_response(response)
    return {"text": result.text, "raw": result.raw}
