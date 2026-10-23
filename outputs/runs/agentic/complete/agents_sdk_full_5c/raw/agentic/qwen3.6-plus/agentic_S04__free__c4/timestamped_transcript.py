"""
Return word or segment timestamps from a transcription result using the AssemblyAI API.

Retrieves a completed transcription with word-level timestamps enabled and
returns the timestamped words and segment boundaries.
"""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List, Optional

from speech_client import (
    create_transcription_request,
    submit_transcription_job,
    upload_audio_file,
    wait_for_completion,
)
from speech_models import normalize_transcription_response, TranscriptResult


def get_timestamped_transcript(
    audio_path: str,
    language_code: str = "en",
) -> Dict[str, Any]:
    """
    Transcribe audio with word-level timestamps via AssemblyAI.

    Parameters
    ----------
    audio_path : str
        Local path to the audio file.
    language_code : str
        Language code for transcription.

    Returns
    -------
    dict
        Contains:
        - text: Full transcript text
        - words: List of word entries with start_ms, end_ms, confidence
        - utterances: List of segment entries with speaker and timestamps
    """
    audio_url = upload_audio_file(audio_path)

    payload = create_transcription_request(
        audio_url=audio_url,
        word_timestamps=True,
        speaker_labels=True,
        language_code=language_code,
        punctuate=True,
    )

    job_id = submit_transcription_job(payload)
    raw_response = wait_for_completion(job_id)

    result: TranscriptResult = normalize_transcription_response(raw_response)

    timestamped_words = []
    for w in result.words:
        timestamped_words.append({
            "text": w.text,
            "start_ms": w.start,
            "end_ms": w.end,
            "confidence": w.confidence,
            "speaker": w.speaker,
        })

    timestamped_utterances = []
    for u in result.utterances:
        timestamped_utterances.append({
            "text": u.text,
            "speaker": u.speaker,
            "start_ms": u.start,
            "end_ms": u.end,
            "word_count": len(u.words),
        })

    return {
        "text": result.text,
        "confidence": result.confidence,
        "language_code": result.language_code,
        "words": timestamped_words,
        "utterances": timestamped_utterances,
    }


def get_word_timestamps_for_segment(
    transcript_data: Dict[str, Any],
    segment_index: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Extract word timestamps for a specific segment or all words.
    """
    if segment_index is not None:
        utterances = transcript_data.get("utterances", [])
        if segment_index < len(utterances):
            start_ms = utterances[segment_index]["start_ms"]
            end_ms = utterances[segment_index]["end_ms"]
            return [
                w for w in transcript_data["words"]
                if w["start_ms"] >= start_ms and w["end_ms"] <= end_ms
            ]
    return transcript_data.get("words", [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Get timestamped transcript")
    parser.add_argument("audio_path", help="Path to the audio file")
    parser.add_argument("--language", default="en", help="Language code")
    parser.add_argument("--segment", type=int, help="Return timestamps for specific segment index")
    args = parser.parse_args()

    transcript_data = get_timestamped_transcript(args.audio_path, args.language)

    if args.segment is not None:
        words = get_word_timestamps_for_segment(transcript_data, args.segment)
        print(json.dumps(words, indent=2))
    else:
        print(json.dumps(transcript_data, indent=2))


if __name__ == "__main__":
    main()
