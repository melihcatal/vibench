# archive_summary.py
import json
from typing import List, Dict


def archive_summary(transcript_results: List[Dict[str, Any]]) -> str:
    """Summarize transcription results for archiving.

    Returns a concise markdown summary.
    """
    summary_lines = ["## Transcription Archive Summary"]
    total_duration = sum([seg.get("duration", 0) for seg in transcript_results])
    total_words = sum([len(seg.get("text", "").split()) for seg in transcript_results])
    summary_lines.append(f"**Total duration:** {total_duration:.2f} seconds")
    summary_lines.append(f"**Total words:** {total_words}")
    # Example: show speaker counts if diarization data present
    speaker_counts = {}
    for seg in transcript_results:
        for word in seg.get("alternatives", [{}])[0].get("timestamps", []):
            speaker = word.get("speaker_tag")
            if speaker:
                speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
    if speaker_counts:
        summary_lines.append("**Speaker distribution:**")
        for sp, count in speaker_counts.items():
            summary_lines.append(f"- Speaker {sp}: {count} words")
    return "\n".join(summary_lines)
