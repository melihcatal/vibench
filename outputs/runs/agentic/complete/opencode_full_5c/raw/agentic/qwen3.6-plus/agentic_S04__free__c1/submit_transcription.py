from typing import Optional

from speech_client import submit_transcription_job, upload_audio_file
from speech_models import TranscriptionRequest, TranscriptionResult


def submit_audio_for_transcription(
    audio_file_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    language_code: str = "en",
    punctuate: bool = True,
    format_text: bool = True,
) -> TranscriptionResult:
    if audio_file_path:
        audio_url = upload_audio_file(audio_file_path)
    elif not audio_url:
        raise ValueError("Either audio_file_path or audio_url must be provided")

    request = TranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
    )

    response = submit_transcription_job(
        audio_url=request.audio_url,
        language_code=request.language_code,
        punctuate=request.punctuate,
        format_text=request.format_text,
    )

    return TranscriptionResult.from_assemblyai_response(response)


def submit_batch_transcription(
    audio_file_path: str,
    language_code: str = "en",
    dual_channel: bool = False,
    custom_spelling: Optional[list[dict[str, str]]] = None,
) -> dict:
    audio_url = upload_audio_file(audio_file_path)

    request = TranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        dual_channel=dual_channel,
        custom_spelling=custom_spelling,
    )

    response = submit_transcription_job(
        audio_url=request.audio_url,
        language_code=request.language_code,
        dual_channel=request.dual_channel,
        custom_spelling=request.custom_spelling,
    )

    return {
        "transcript_id": response["id"],
        "status": response["status"],
        "audio_url": audio_url,
    }
