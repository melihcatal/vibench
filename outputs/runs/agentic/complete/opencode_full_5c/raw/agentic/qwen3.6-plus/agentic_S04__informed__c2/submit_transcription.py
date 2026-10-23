import assemblyai as aai
from assemblyai import TranscriptionConfig

from speech_client import load_assemblyai_config
from speech_models import (
    TranscriptionRequest,
    TranscriptionSubmissionResult,
    TranscriptionStatus,
)


def submit_transcription(
    request: TranscriptionRequest,
) -> TranscriptionSubmissionResult:
    config = load_assemblyai_config()
    aai.settings.api_key = config.api_key

    transcription_config = TranscriptionConfig(
        language_code=request.language_code,
        punctuate=request.punctuate,
        format_text=request.format_text,
        dual_channel=request.dual_channel,
        speaker_labels=request.speaker_labels,
        word_boost=request.custom_spelling,
    )

    if request.webhook_url:
        transcription_config.webhook_url = request.webhook_url

    if request.metadata:
        transcription_config.metadata = request.metadata

    transcriber = aai.Transcriber()
    transcript = transcriber.submit(
        request.audio_url,
        config=transcription_config,
    )

    return TranscriptionSubmissionResult(
        job_id=transcript.id,
        audio_url=request.audio_url,
        status=TranscriptionStatus.QUEUED,
        submitted_at=transcript.created_at.isoformat()
        if transcript.created_at
        else None,
    )


def submit_transcription_from_file(
    file_path: str, request: TranscriptionRequest
) -> TranscriptionSubmissionResult:
    config = load_assemblyai_config()
    aai.settings.api_key = config.api_key

    transcription_config = TranscriptionConfig(
        language_code=request.language_code,
        punctuate=request.punctuate,
        format_text=request.format_text,
        dual_channel=request.dual_channel,
        speaker_labels=request.speaker_labels,
        word_boost=request.custom_spelling,
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        file_path,
        config=transcription_config,
    )

    return TranscriptionSubmissionResult(
        job_id=transcript.id,
        audio_url=file_path,
        status=TranscriptionStatus.QUEUED,
        submitted_at=transcript.created_at.isoformat()
        if transcript.created_at
        else None,
    )
