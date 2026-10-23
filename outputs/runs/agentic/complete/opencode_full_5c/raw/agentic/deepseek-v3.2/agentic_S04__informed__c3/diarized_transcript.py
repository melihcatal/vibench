import os
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import DiarizationRequest, DiarizationResult


def request_diarization(
    audio_file_path: str, max_speakers: int = 10
) -> DiarizationResult:
    """
    Request speaker diarization for a recorded meeting using Amazon Transcribe.

    Args:
        audio_file_path: Path to the audio file
        max_speakers: Maximum number of speakers to identify

    Returns:
        DiarizationResult with speaker segments
    """
    client = get_speech_client()

    # Generate a unique job name
    import uuid

    job_name = f"diarization-job-{uuid.uuid4().hex[:8]}"

    # Upload audio file to S3
    s3_client = boto3.client("s3")
    bucket_name = os.environ.get("AWS_TRANSCRIBE_BUCKET", "transcription-audio-bucket")

    try:
        # Upload to S3
        s3_key = f"audio/{job_name}.wav"
        s3_client.upload_file(audio_file_path, bucket_name, s3_key)

        # Start transcription job with speaker diarization enabled
        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode="en-US",
            MediaFormat="wav",
            Media={"MediaFileUri": f"s3://{bucket_name}/{s3_key}"},
            Settings={
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": max_speakers,
                "ChannelIdentification": False,  # Set to True for separate channel audio
            },
        )

        job_id = response["TranscriptionJob"]["TranscriptionJobName"]

        # Return result with job ID for polling
        return DiarizationResult(
            job_id=job_id,
            audio_file=audio_file_path,
            max_speakers=max_speakers,
            status="SUBMITTED",
        )

    except ClientError as e:
        print(f"Error requesting diarization: {e}")
        raise


def get_diarization_result(job_id: str) -> DiarizationResult:
    """
    Get diarization results for a completed job.

    Args:
        job_id: Transcription job ID

    Returns:
        DiarizationResult with speaker segments
    """
    client = get_speech_client()

    try:
        response = client.get_transcription_job(TranscriptionJobName=job_id)

        if response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED":
            return DiarizationResult(job_id=job_id, status="IN_PROGRESS")

        # Get the transcript from S3
        import json
        import urllib.request

        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcript_data = json.loads(urllib.request.urlopen(transcript_uri).read())

        # Extract speaker segments
        speaker_segments = []
        if "speaker_labels" in transcript_data["results"]:
            for segment in transcript_data["results"]["speaker_labels"]["segments"]:
                speaker_segments.append(
                    {
                        "speaker_label": segment["speaker_label"],
                        "start_time": float(segment["start_time"]),
                        "end_time": float(segment["end_time"]),
                        "items": [],
                    }
                )

        # Map words to speaker segments
        if "items" in transcript_data["results"]:
            for item in transcript_data["results"]["items"]:
                if item["type"] == "pronunciation":
                    # Find which speaker segment this word belongs to
                    word_start = float(item["start_time"])
                    for segment in speaker_segments:
                        if segment["start_time"] <= word_start <= segment["end_time"]:
                            segment["items"].append(
                                {
                                    "word": item["alternatives"][0]["content"],
                                    "start_time": word_start,
                                    "end_time": float(item["end_time"]),
                                    "confidence": float(
                                        item["alternatives"][0]["confidence"]
                                    ),
                                }
                            )
                            break

        return DiarizationResult(
            job_id=job_id,
            speaker_segments=speaker_segments,
            total_speakers=len(set(seg["speaker_label"] for seg in speaker_segments)),
            status="COMPLETED",
            raw_response=transcript_data,
        )

    except ClientError as e:
        print(f"Error getting diarization result: {e}")
        raise


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        result = request_diarization(sys.argv[1])
        print(f"Diarization job submitted: {result.job_id}")
    else:
        print("Usage: python diarized_transcript.py <audio_file_path>")
