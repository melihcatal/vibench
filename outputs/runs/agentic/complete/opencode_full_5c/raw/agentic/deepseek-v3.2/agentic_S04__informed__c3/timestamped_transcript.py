import os
import json
import urllib.request
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import TimestampedTranscript


def get_timestamped_transcript(job_id: str) -> TimestampedTranscript:
    """
    Return word or segment timestamps from a transcription result.

    Args:
        job_id: Transcription job ID

    Returns:
        TimestampedTranscript with word timestamps and segments
    """
    client = get_speech_client()

    try:
        response = client.get_transcription_job(TranscriptionJobName=job_id)

        if response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED":
            raise Exception(f"Transcription job {job_id} is not completed")

        # Get the transcript from S3
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcript_data = json.loads(urllib.request.urlopen(transcript_uri).read())

        # Extract word timestamps
        word_timestamps = []
        if "items" in transcript_data["results"]:
            for item in transcript_data["results"]["items"]:
                if item["type"] == "pronunciation":
                    word_timestamps.append(
                        {
                            "word": item["alternatives"][0]["content"],
                            "start_time": float(item["start_time"]),
                            "end_time": float(item["end_time"]),
                            "confidence": float(item["alternatives"][0]["confidence"]),
                        }
                    )

        # Extract segment timestamps (group consecutive words)
        segments = []
        current_segment = None

        for word in word_timestamps:
            if current_segment is None:
                current_segment = {
                    "text": word["word"],
                    "start_time": word["start_time"],
                    "end_time": word["end_time"],
                    "words": [word],
                }
            elif (
                word["start_time"] - current_segment["end_time"] < 1.0
            ):  # Group if gap < 1 second
                current_segment["text"] += " " + word["word"]
                current_segment["end_time"] = word["end_time"]
                current_segment["words"].append(word)
            else:
                segments.append(current_segment)
                current_segment = {
                    "text": word["word"],
                    "start_time": word["start_time"],
                    "end_time": word["end_time"],
                    "words": [word],
                }

        if current_segment is not None:
            segments.append(current_segment)

        # Extract speaker segments if available
        speaker_segments = []
        if "speaker_labels" in transcript_data["results"]:
            for segment in transcript_data["results"]["speaker_labels"]["segments"]:
                speaker_segments.append(
                    {
                        "speaker_label": segment["speaker_label"],
                        "start_time": float(segment["start_time"]),
                        "end_time": float(segment["end_time"]),
                    }
                )

        return TimestampedTranscript(
            job_id=job_id,
            word_timestamps=word_timestamps,
            segments=segments,
            speaker_segments=speaker_segments,
            full_transcript=transcript_data["results"]["transcripts"][0]["transcript"],
            raw_response=transcript_data,
        )

    except ClientError as e:
        print(f"Error getting timestamped transcript: {e}")
        raise


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        result = get_timestamped_transcript(sys.argv[1])
        print(f"Full transcript: {result.full_transcript}")
        print(f"\nWord timestamps:")
        for word in result.word_timestamps[:10]:  # Show first 10 words
            print(
                f"{format_timestamp(word['start_time'])} - {word['word']} (conf: {word['confidence']:.2f})"
            )
    else:
        print("Usage: python timestamped_transcript.py <job_id>")
