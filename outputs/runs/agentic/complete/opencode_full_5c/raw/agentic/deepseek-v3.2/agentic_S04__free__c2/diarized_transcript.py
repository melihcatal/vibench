import os
import boto3
from botocore.exceptions import ClientError
from speech_client import get_speech_client
from speech_models import DiarizationRequest


def diarized_transcript(audio_file_path: str, max_speakers: int = 2) -> dict:
    """
    Request speaker diarization for a recorded meeting using AWS Transcribe.

    Args:
        audio_file_path: Path to the audio file
        max_speakers: Maximum number of speakers to identify

    Returns:
        Dictionary containing diarization results
    """
    client = get_speech_client()

    # Upload audio file to S3
    s3_client = boto3.client("s3")
    bucket_name = os.environ.get("AWS_TRANSCRIBE_BUCKET", "transcription-audio-bucket")

    import uuid

    audio_key = f"audio/{uuid.uuid4()}_{os.path.basename(audio_file_path)}"

    try:
        # Upload audio to S3
        s3_client.upload_file(audio_file_path, bucket_name, audio_key)

        # Create transcription job with speaker diarization
        job_name = f"diarization-job-{uuid.uuid4()}"
        media_uri = f"s3://{bucket_name}/{audio_key}"

        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_uri},
            MediaFormat=audio_file_path.split(".")[-1].lower(),
            LanguageCode="en-US",
            Settings={
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": max_speakers,
                "ChannelIdentification": False,
            },
        )

        job_id = response["TranscriptionJob"]["TranscriptionJobName"]

        # Poll for completion
        import time

        timeout_seconds = 300

        for _ in range(timeout_seconds // 5):
            job_response = client.get_transcription_job(TranscriptionJobName=job_id)
            status = job_response["TranscriptionJob"]["TranscriptionJobStatus"]

            if status == "COMPLETED":
                # Get the transcript with speaker labels
                transcript_uri = job_response["TranscriptionJob"]["Transcript"][
                    "TranscriptFileUri"
                ]

                import json
                import urllib.request

                transcript_data = json.loads(
                    urllib.request.urlopen(transcript_uri).read()
                )

                # Extract speaker diarization results
                speaker_segments = []
                if "speaker_labels" in transcript_data["results"]:
                    speaker_labels = transcript_data["results"]["speaker_labels"][
                        "segments"
                    ]

                    for segment in speaker_labels:
                        speaker_segments.append(
                            {
                                "start_time": segment["start_time"],
                                "end_time": segment["end_time"],
                                "speaker_label": segment["speaker_label"],
                                "items": [],
                            }
                        )

                # Map items to speaker segments
                if "items" in transcript_data["results"]:
                    items = transcript_data["results"]["items"]

                    for item in items:
                        if "start_time" in item and "end_time" in item:
                            for segment in speaker_segments:
                                if float(item["start_time"]) >= float(
                                    segment["start_time"]
                                ) and float(item["end_time"]) <= float(
                                    segment["end_time"]
                                ):
                                    segment["items"].append(item)
                                    break

                return {
                    "job_id": job_id,
                    "speaker_segments": speaker_segments,
                    "transcript": transcript_data["results"]["transcripts"][0][
                        "transcript"
                    ],
                    "total_speakers": len(
                        set([s["speaker_label"] for s in speaker_segments])
                    ),
                }

            elif status == "FAILED":
                failure_reason = job_response["TranscriptionJob"].get(
                    "FailureReason", "Unknown error"
                )
                raise Exception(f"Diarization job failed: {failure_reason}")

            time.sleep(5)

        raise TimeoutError(
            f"Diarization job {job_id} did not complete within {timeout_seconds} seconds"
        )

    except ClientError as e:
        print(f"Error requesting diarization: {e}")
        raise
