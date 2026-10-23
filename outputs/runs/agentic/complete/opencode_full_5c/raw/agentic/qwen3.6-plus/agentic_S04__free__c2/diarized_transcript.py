import sys
import json
from typing import Optional, List, Dict, Any

from speech_models import (
    TranscriptionRequest,
    TranscriptionResult,
    UtteranceInfo,
)
from speech_client import (
    submit_transcription_job,
    poll_until_complete,
    get_assemblyai_config,
)


def request_diarized_transcript(
    audio_file_path: str,
    language_code: Optional[str] = None,
    speakers_expected: Optional[int] = None,
    poll_interval: float = 5.0,
    max_wait: float = 600.0,
) -> Dict[str, Any]:
    config = get_assemblyai_config()
    extra_params = {}
    if speakers_expected is not None:
        extra_params["speakers_expected"] = speakers_expected
    request = TranscriptionRequest(
        audio_file_path=audio_file_path,
        speaker_labels=True,
        word_timestamps=True,
        language_code=language_code,
        extra_params=extra_params,
    )
    job = submit_transcription_job(request, config)
    result = poll_until_complete(
        job.job_id, config, interval=poll_interval, max_wait=max_wait
    )
    return format_diarized_output(result)


def format_diarized_output(result: TranscriptionResult) -> Dict[str, Any]:
    speakers: Dict[str, List[Dict[str, Any]]] = {}
    for utterance in result.utterances:
        speaker = utterance.speaker or "unknown"
        if speaker not in speakers:
            speakers[speaker] = []
        speakers[speaker].append(
            {
                "text": utterance.text,
                "start_ms": utterance.start,
                "end_ms": utterance.end,
                "word_count": len(utterance.words),
                "confidence": utterance.confidence,
            }
        )
    speaker_summary = []
    for speaker_id, utterances in speakers.items():
        total_duration = (
            max(u["end_ms"] for u in utterances)
            - min(u["start_ms"] for u in utterances)
            if utterances
            else 0
        )
        speaker_summary.append(
            {
                "speaker": speaker_id,
                "utterance_count": len(utterances),
                "total_duration_ms": total_duration,
            }
        )
    return {
        "job_id": result.job_id,
        "audio_duration_ms": int(result.audio_duration * 1000),
        "speaker_count": len(speakers),
        "speakers": speaker_summary,
        "transcript": [
            {
                "speaker": u.speaker,
                "text": u.text,
                "start_ms": u.start,
                "end_ms": u.end,
                "confidence": u.confidence,
            }
            for u in result.utterances
        ],
    }


def get_diarized_transcript(
    job_id: str,
    poll_interval: float = 5.0,
    max_wait: float = 600.0,
) -> Dict[str, Any]:
    config = get_assemblyai_config()
    result = poll_until_complete(
        job_id, config, interval=poll_interval, max_wait=max_wait
    )
    return format_diarized_output(result)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python diarized_transcript.py <audio_file_path> [speakers_expected]"
        )
        sys.exit(1)
    audio_file_path = sys.argv[1]
    speakers_expected = int(sys.argv[2]) if len(sys.argv) > 2 else None
    result = request_diarized_transcript(
        audio_file_path, speakers_expected=speakers_expected
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
