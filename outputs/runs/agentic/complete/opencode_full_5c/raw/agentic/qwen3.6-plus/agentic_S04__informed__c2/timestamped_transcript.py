import assemblyai as aai
from assemblyai import TranscriptionConfig

from speech_client import load_assemblyai_config
from speech_models import (
    TranscriptionResult,
    TranscriptionStatus,
    UtteranceSegment,
    WordSegment,
)


def get_timestamped_transcript(audio_url: str) -> TranscriptionResult:
    config = load_assemblyai_config()
    aai.settings.api_key = config.api_key

    transcription_config = TranscriptionConfig(
        language_code=config.default_language_code,
        punctuate=True,
        format_text=True,
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        audio_url,
        config=transcription_config,
    )

    if transcript.status != aai.TranscriptStatus.completed:
        raise RuntimeError(
            f"Transcription did not complete. Status: {transcript.status}"
        )

    words_list = [
        WordSegment(
            text=w.text,
            start_ms=w.start,
            end_ms=w.end,
            confidence=w.confidence,
        )
        for w in transcript.words
    ]

    utterances = []
    for utt in transcript.utterances:
        utt_words = [
            WordSegment(
                text=w.text,
                start_ms=w.start,
                end_ms=w.end,
                confidence=w.confidence,
            )
            for w in utt.words
        ]
        utterances.append(
            UtteranceSegment(
                text=utt.text,
                start_ms=utt.start,
                end_ms=utt.end,
                words=utt_words,
                confidence=utt.confidence,
            )
        )

    return TranscriptionResult(
        job_id=transcript.id,
        status=TranscriptionStatus.COMPLETED,
        text=transcript.text,
        utterances=utterances,
        words=words_list,
        audio_duration_ms=int(transcript.audio_duration * 1000)
        if transcript.audio_duration
        else 0,
        language=transcript.language_code or "",
        confidence=transcript.confidence or 0.0,
    )


def get_timestamped_transcript_by_job(job_id: str) -> TranscriptionResult:
    config = load_assemblyai_config()
    aai.settings.api_key = config.api_key

    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcription(job_id)

    if transcript.status != aai.TranscriptStatus.completed:
        raise RuntimeError(
            f"Transcription job {job_id} is not completed. Status: {transcript.status}"
        )

    words_list = [
        WordSegment(
            text=w.text,
            start_ms=w.start,
            end_ms=w.end,
            confidence=w.confidence,
        )
        for w in transcript.words
    ]

    utterances = []
    for utt in transcript.utterances:
        utt_words = [
            WordSegment(
                text=w.text,
                start_ms=w.start,
                end_ms=w.end,
                confidence=w.confidence,
            )
            for w in utt.words
        ]
        utterances.append(
            UtteranceSegment(
                text=utt.text,
                start_ms=utt.start,
                end_ms=utt.end,
                words=utt_words,
                confidence=utt.confidence,
            )
        )

    return TranscriptionResult(
        job_id=transcript.id,
        status=TranscriptionStatus.COMPLETED,
        text=transcript.text,
        utterances=utterances,
        words=words_list,
        audio_duration_ms=int(transcript.audio_duration * 1000)
        if transcript.audio_duration
        else 0,
        language=transcript.language_code or "",
        confidence=transcript.confidence or 0.0,
    )


def extract_word_segments(transcript_result: TranscriptionResult) -> list:
    return transcript_result.words


def extract_segment_timestamps(transcript_result: TranscriptionResult) -> list:
    return [
        {
            "text": utt.text,
            "start_ms": utt.start_ms,
            "end_ms": utt.end_ms,
            "speaker": utt.speaker,
        }
        for utt in transcript_result.utterances
    ]
