from typing import Optional, List, Dict, Any

from speech_client import create_assemblyai_session, poll_until_complete
from speech_models import TranscriptionResult, WordSegment


def get_timestamped_transcript(
    transcript_id: str,
    granularity: str = "word",
) -> Dict[str, Any]:
    session = create_assemblyai_session()
    result_data = poll_until_complete(session, transcript_id)
    transcription = TranscriptionResult.from_assemblyai_response(result_data)

    if granularity == "word":
        segments = []
        for word in transcription.words:
            segments.append(
                {
                    "text": word.text,
                    "start_ms": word.start,
                    "end_ms": word.end,
                    "confidence": word.confidence,
                    "speaker": word.speaker,
                }
            )
    elif granularity == "utterance":
        segments = []
        for utt in transcription.utterances:
            segments.append(
                {
                    "text": utt.text,
                    "start_ms": utt.start,
                    "end_ms": utt.end,
                    "confidence": utt.confidence,
                    "speaker": utt.speaker,
                    "word_count": len(utt.words),
                }
            )
    else:
        raise ValueError(
            f"Unsupported granularity: {granularity}. Use 'word' or 'utterance'."
        )

    return {
        "transcript_id": transcription.transcript_id,
        "granularity": granularity,
        "total_segments": len(segments),
        "audio_duration_ms": int(transcription.audio_duration * 1000),
        "segments": segments,
    }


def format_timestamped_text(
    segments: List[Dict[str, Any]], include_speaker: bool = True
) -> str:
    lines = []
    for seg in segments:
        start_sec = seg["start_ms"] / 1000
        end_sec = seg["end_ms"] / 1000
        timestamp = f"[{start_sec:.2f}-{end_sec:.2f}]"
        speaker_tag = (
            f" [{seg.get('speaker', 'unknown')}]"
            if include_speaker and seg.get("speaker")
            else ""
        )
        lines.append(f"{timestamp}{speaker_tag} {seg['text']}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    tid = sys.argv[1] if len(sys.argv) > 1 else None
    if not tid:
        print(
            "Usage: python timestamped_transcript.py <transcript_id> [word|utterance]"
        )
        sys.exit(1)

    gran = sys.argv[2] if len(sys.argv) > 2 else "word"
    result = get_timestamped_transcript(tid, granularity=gran)
    print(format_timestamped_text(result["segments"]))
