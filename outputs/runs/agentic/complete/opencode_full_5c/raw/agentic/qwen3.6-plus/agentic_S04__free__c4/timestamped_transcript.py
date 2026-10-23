import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import TimestampedResult, normalize_timestamp_response


def get_timestamped_transcript(audio_url: str) -> TimestampedResult:
    aai.settings.api_key = get_assemblyai_client().api_key
    config = aai.TranscriptionConfig(
        word_boost=[],
        punctuate=True,
        format_text=True,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config)
    if transcript.status == aai.TranscriptStatus.error:
        return TimestampedResult(job_id="", text="", words=[], segments=[])
    raw = {
        "id": transcript.id,
        "text": transcript.text,
        "segments": [
            {
                "text": word.text,
                "start": word.start / 1000.0,
                "end": word.end / 1000.0,
                "confidence": word.confidence,
                "words": [
                    {
                        "word": word.text,
                        "start": word.start / 1000.0,
                        "end": word.end / 1000.0,
                        "confidence": word.confidence,
                    }
                ],
            }
            for word in transcript.words or []
        ],
    }
    return normalize_timestamp_response(raw)


def get_word_timestamps(audio_url: str) -> list[dict]:
    aai.settings.api_key = get_assemblyai_client().api_key
    config = aai.TranscriptionConfig(
        word_boost=[],
        punctuate=True,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config)
    if transcript.status == aai.TranscriptStatus.error:
        return []
    return [
        {
            "word": word.text,
            "start": word.start / 1000.0,
            "end": word.end / 1000.0,
            "confidence": word.confidence,
        }
        for word in transcript.words or []
    ]
