import assemblyai as aai
from assemblyai import TranscriptionConfig

from speech_client import load_assemblyai_config
from speech_models import (
    TranscriptionRequest,
    TranscriptionResult,
    TranscriptionStatus,
    UtteranceSegment,
    WordSegment,
)


def request_diarized_transcription(
    audio_url: str, speaker_count: int = None
) -> TranscriptionResult:
    config = load_assemblyai_config()
    aai.settings.api_key = config.api_key

    transcription_config = TranscriptionConfig(
        language_code=config.default_language_code,
        speaker_labels=True,
        punctuate=True,
        format_text=True,
    )

    if speaker_count is not None:
        transcription_config.speakers_expected = speaker_count

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        audio_url,
        config=transcription_config,
    )

    utterances = []
    for utt in transcript.utterances:
        words = [
            WordSegment(
                text=w.text,
                start_ms=w.start,
                end_ms=w.end,
                confidence=w.confidence,
                speaker=utt.speaker,
            )
            for w in utt.words
        ]
        utterances.append(
            UtteranceSegment(
                text=utt.text,
                speaker=utt.speaker,
                start_ms=utt.start,
                end_ms=utt.end,
                words=words,
                confidence=utt.confidence,
            )
        )

    return TranscriptionResult(
        job_id=transcript.id,
        status=TranscriptionStatus.COMPLETED,
        text=transcript.text,
        utterances=utterances,
        audio_duration_ms=int(transcript.audio_duration * 1000)
        if transcript.audio_duration
        else 0,
        language=transcript.language_code or "",
        confidence=transcript.confidence or 0.0,
    )


def get_diarized_transcript_by_job(job_id: str) -> TranscriptionResult:
    config = load_assemblyai_config()
    aai.settings.api_key = config.api_key

    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcription(job_id)

    if transcript.status != aai.TranscriptStatus.completed:
        raise RuntimeError(
            f"Transcription job {job_id} is not completed. Status: {transcript.status}"
        )

    utterances = []
    for utt in transcript.utterances:
        words = [
            WordSegment(
                text=w.text,
                start_ms=w.start,
                end_ms=w.end,
                confidence=w.confidence,
                speaker=utt.speaker,
            )
            for w in utt.words
        ]
        utterances.append(
            UtteranceSegment(
                text=utt.text,
                speaker=utt.speaker,
                start_ms=utt.start,
                end_ms=utt.end,
                words=words,
                confidence=utt.confidence,
            )
        )

    return TranscriptionResult(
        job_id=transcript.id,
        status=TranscriptionStatus.COMPLETED,
        text=transcript.text,
        utterances=utterances,
        audio_duration_ms=int(transcript.audio_duration * 1000)
        if transcript.audio_duration
        else 0,
        language=transcript.language_code or "",
        confidence=transcript.confidence or 0.0,
    )
