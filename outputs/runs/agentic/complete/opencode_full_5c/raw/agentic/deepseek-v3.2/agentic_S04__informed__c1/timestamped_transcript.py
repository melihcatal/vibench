import boto3
import json
from typing import Dict, Any, List, Tuple
import urllib.request


def get_timestamped_transcript(job_name: str) -> List[Dict[str, Any]]:
    """
    Return word or segment timestamps from a transcription result.

    Args:
        job_name: Name of the transcription job

    Returns:
        List of timestamped words/segments
    """
    transcribe_client = boto3.client("transcribe")

    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)

    if response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED":
        raise ValueError(f"Job {job_name} is not completed")

    transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

    with urllib.request.urlopen(transcript_uri) as url:
        transcript_data = json.loads(url.read().decode())

    items = transcript_data["results"].get("items", [])

    timestamped_words = []

    for item in items:
        if item["type"] == "pronunciation":
            word_info = {
                "word": item["alternatives"][0]["content"],
                "start_time": float(item.get("start_time", 0)),
                "end_time": float(item.get("end_time", 0)),
                "confidence": float(item["alternatives"][0].get("confidence", 0)),
                "type": "word",
            }
            timestamped_words.append(word_info)

    return timestamped_words


def get_segmented_transcript(
    job_name: str, segment_duration: float = 30.0
) -> List[Dict[str, Any]]:
    """
    Get transcript divided into time segments.

    Args:
        job_name: Name of the transcription job
        segment_duration: Duration of each segment in seconds

    Returns:
        List of transcript segments
    """
    timestamped_words = get_timestamped_transcript(job_name)

    if not timestamped_words:
        return []

    segments = []
    current_segment = []
    segment_start = timestamped_words[0]["start_time"]

    for word in timestamped_words:
        if word["start_time"] - segment_start >= segment_duration and current_segment:
            segment_text = " ".join([w["word"] for w in current_segment])
            segments.append(
                {
                    "start_time": segment_start,
                    "end_time": current_segment[-1]["end_time"],
                    "text": segment_text,
                    "word_count": len(current_segment),
                    "words": current_segment.copy(),
                }
            )
            current_segment = []
            segment_start = word["start_time"]

        current_segment.append(word)

    if current_segment:
        segment_text = " ".join([w["word"] for w in current_segment])
        segments.append(
            {
                "start_time": segment_start,
                "end_time": current_segment[-1]["end_time"],
                "text": segment_text,
                "word_count": len(current_segment),
                "words": current_segment.copy(),
            }
        )

    return segments


def get_transcript_with_timestamps(job_name: str) -> str:
    """
    Get transcript with timestamps formatted for readability.

    Args:
        job_name: Name of the transcription job

    Returns:
        Formatted transcript with timestamps
    """
    segments = get_segmented_transcript(job_name, segment_duration=10.0)

    formatted_lines = []
    for segment in segments:
        start_min = int(segment["start_time"] // 60)
        start_sec = int(segment["start_time"] % 60)
        end_min = int(segment["end_time"] // 60)
        end_sec = int(segment["end_time"] % 60)

        timestamp = f"[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}]"
        formatted_lines.append(f"{timestamp} {segment['text']}")

    return "\n".join(formatted_lines)
