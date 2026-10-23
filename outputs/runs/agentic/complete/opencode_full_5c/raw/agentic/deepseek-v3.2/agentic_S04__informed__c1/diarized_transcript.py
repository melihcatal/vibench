import boto3
import json
import os
from typing import Dict, Any, List, Optional


def submit_diarized_transcription(
    audio_file_path: str, max_speakers: int = 2, language_code: str = "en-US"
) -> Dict[str, Any]:
    """
    Request speaker diarization for a recorded meeting using Amazon Transcribe.

    Args:
        audio_file_path: Path to the audio file (local or S3 URI)
        max_speakers: Maximum number of speakers to identify
        language_code: Language code for transcription

    Returns:
        Dictionary with job details and diarization settings
    """
    transcribe_client = boto3.client("transcribe")

    import uuid

    job_name = f"diarized-meeting-{uuid.uuid4().hex[:8]}"

    media_format = audio_file_path.split(".")[-1].lower()
    if media_format not in ["mp3", "mp4", "wav", "flac", "ogg", "amr", "webm"]:
        media_format = "mp3"

    if audio_file_path.startswith("s3://"):
        media_uri = audio_file_path
    else:
        s3_client = boto3.client("s3")
        bucket_name = os.environ.get(
            "AWS_TRANSCRIBE_BUCKET", "transcription-audio-bucket"
        )
        object_key = f"meetings/{job_name}.{media_format}"

        s3_client.upload_file(audio_file_path, bucket_name, object_key)
        media_uri = f"s3://{bucket_name}/{object_key}"

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat=media_format,
        Media={"MediaFileUri": media_uri},
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": max_speakers,
            "ChannelIdentification": False,
        },
        ContentRedaction={
            "RedactionType": "PII",
            "RedactionOutput": "redacted_and_unredacted",
        }
        if language_code == "en-US"
        else {},
    )

    return {
        "job_name": job_name,
        "max_speakers": max_speakers,
        "media_uri": media_uri,
        "language_code": language_code,
        "status": "SUBMITTED",
    }


def get_diarized_transcript(job_name: str) -> List[Dict[str, Any]]:
    """
    Get diarized transcript with speaker labels.

    Args:
        job_name: Name of the transcription job

    Returns:
        List of transcript segments with speaker labels
    """
    import urllib.request
    import time

    transcribe_client = boto3.client("transcribe")

    for _ in range(30):
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )

        status = response["TranscriptionJob"]["TranscriptionJobStatus"]

        if status == "COMPLETED":
            transcript_uri = response["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]

            with urllib.request.urlopen(transcript_uri) as url:
                transcript_data = json.loads(url.read().decode())

            items = transcript_data["results"].get("items", [])
            speaker_segments = (
                transcript_data["results"].get("speaker_labels", {}).get("segments", [])
            )

            diarized_segments = []

            for segment in speaker_segments:
                start_time = float(segment["start_time"])
                end_time = float(segment["end_time"])
                speaker_label = segment["speaker_label"]

                segment_items = [
                    item
                    for item in items
                    if float(item.get("start_time", 0)) >= start_time
                    and float(item.get("end_time", 0)) <= end_time
                ]

                segment_text = " ".join(
                    [item["alternatives"][0]["content"] for item in segment_items]
                )

                diarized_segments.append(
                    {
                        "speaker": speaker_label,
                        "start_time": start_time,
                        "end_time": end_time,
                        "text": segment_text,
                        "items": segment_items,
                    }
                )

            return diarized_segments

        elif status == "FAILED":
            raise Exception("Transcription job failed")

        time.sleep(5)

    raise TimeoutError("Transcription job timed out")
