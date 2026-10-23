import json
import urllib.request
from speech_client import get_speech_client
from speech_models import TimestampedTranscript


def timestamped_transcript(job_id: str) -> TimestampedTranscript:
    """
    Return word or segment timestamps from a transcription result.

    Args:
        job_id: Transcription job ID

    Returns:
        TimestampedTranscript object with word-level timestamps
    """
    client = get_speech_client()

    try:
        # Get the transcription job
        response = client.get_transcription_job(TranscriptionJobName=job_id)

        if response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED":
            raise Exception(f"Transcription job {job_id} is not completed")

        # Get the transcript from the output URI
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcript_data = json.loads(urllib.request.urlopen(transcript_uri).read())

        # Extract word-level timestamps
        word_timestamps = []
        segment_timestamps = []

        if "items" in transcript_data["results"]:
            items = transcript_data["results"]["items"]

            for item in items:
                if item["type"] == "pronunciation":
                    word_timestamps.append(
                        {
                            "word": item["alternatives"][0]["content"],
                            "start_time": float(item["start_time"]),
                            "end_time": float(item["end_time"]),
                            "confidence": float(
                                item["alternatives"][0].get("confidence", 0.0)
                            ),
                        }
                    )
                elif item["type"] == "punctuation":
                    # Handle punctuation marks
                    pass

        # Extract segment timestamps if available
        if "segments" in transcript_data["results"]:
            segments = transcript_data["results"]["segments"]
            for segment in segments:
                segment_timestamps.append(
                    {
                        "text": segment["alternatives"][0]["transcript"],
                        "start_time": float(segment["start_time"]),
                        "end_time": float(segment["end_time"]),
                        "speaker_label": segment.get("speaker_label", "spk_0"),
                    }
                )

        # If no segments but we have speaker labels, create segments from speaker labels
        elif "speaker_labels" in transcript_data["results"] and word_timestamps:
            speaker_labels = transcript_data["results"]["speaker_labels"]["segments"]

            for label in speaker_labels:
                # Find words within this speaker segment
                segment_words = []
                for word in word_timestamps:
                    if word["start_time"] >= float(label["start_time"]) and word[
                        "end_time"
                    ] <= float(label["end_time"]):
                        segment_words.append(word["word"])

                if segment_words:
                    segment_timestamps.append(
                        {
                            "text": " ".join(segment_words),
                            "start_time": float(label["start_time"]),
                            "end_time": float(label["end_time"]),
                            "speaker_label": label["speaker_label"],
                        }
                    )

        return TimestampedTranscript(
            job_id=job_id,
            word_timestamps=word_timestamps,
            segment_timestamps=segment_timestamps,
            full_transcript=transcript_data["results"]["transcripts"][0]["transcript"],
        )

    except Exception as e:
        print(f"Error getting timestamped transcript: {e}")
        raise
