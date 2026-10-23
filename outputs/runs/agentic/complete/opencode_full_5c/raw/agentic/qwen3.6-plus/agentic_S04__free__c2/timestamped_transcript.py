import sys
import json
from typing import Optional, List, Dict, Any

from speech_models import (
    TranscriptionRequest,
    TranscriptionResult,
    WordInfo,
)
from speech_client import (
    submit_transcription_job,
    poll_until_complete,
    get_transcription_result,
    get_assemblyai_config,
)


def request_timestamped_transcript(
    audio_file_path: str,
    language_code: Optional[str] = None,
    poll_interval: float = 5.0,
    max_wait: float = 600.0,
) -> Dict[str, Any]:
    config = get_assemblyai_config()
    request = TranscriptionRequest(
        audio_file_path=audio_file_path,
        word_timestamps=True,
        speaker_labels=True,
        language_code=language_code,
    )
    job = submit_transcription_job(request, config)
    result = poll_until_complete(
        job.job_id, config, interval=poll_interval, max_wait=max_wait
    )
    return format_timestamped_output(result)


def format_timestamped_output(result: TranscriptionResult) -> Dict[str, Any]:
    word_segments = [
        {
            "text": w.text,
            "start_ms": w.start,
            "end_ms": w.end,
            "confidence": w.confidence,
            "speaker": w.speaker,
        }
        for w in result.words
    ]
    utterance_segments = [
        {
            "text": u.text,
            "start_ms": u.start,
            "end_ms": u.end,
            "speaker": u.speaker,
            "word_count": len(u.words),
            "confidence": u.confidence,
        }
        for u in result.utterances
    ]
    return {
        "job_id": result.job_id,
        "audio_duration_ms": int(result.audio_duration * 1000),
        "full_text": result.text,
        "word_segments": word_segments,
        "utterance_segments": utterance_segments,
        "total_words": len(word_segments),
        "total_utterances": len(utterance_segments),
    }


def get_word_timestamps(
    job_id: str,
    poll_interval: float = 5.0,
    max_wait: float = 600.0,
) -> List[Dict[str, Any]]:
    config = get_assemblyai_config()
    result = poll_until_complete(
        job_id, config, interval=poll_interval, max_wait=max_wait
    )
    return [
        {
            "text": w.text,
            "start_ms": w.start,
            "end_ms": w.end,
            "confidence": w.confidence,
            "speaker": w.speaker,
        }
        for w in result.words
    ]


def get_segment_timestamps(
    job_id: str,
    poll_interval: float = 5.0,
    max_wait: float = 600.0,
) -> List[Dict[str, Any]]:
    config = get_assemblyai_config()
    result = poll_until_complete(
        job_id, config, interval=poll_interval, max_wait=max_wait
    )
    return [
        {
            "text": u.text,
            "start_ms": u.start,
            "end_ms": u.end,
            "speaker": u.speaker,
            "word_count": len(u.words),
            "confidence": u.confidence,
        }
        for u in result.utterances
    ]


def main():
    if len(sys.argv) < 2:
        print("Usage: python timestamped_transcript.py <audio_file_path>")
        sys.exit(1)
    audio_file_path = sys.argv[1]
    result = request_timestamped_transcript(audio_file_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
