import os
import time
import json
import requests
from speech_client import get_transcribe_client, get_s3_client
from speech_models import TranscriptionJobResult


def poll_transcription_job(
    job_name: str, poll_interval_seconds: int = 10
) -> TranscriptionJobResult:
    """
    Polls the status of a transcription job and returns the transcript when completed.

    Args:
        job_name: The name of the transcription job to poll.
        poll_interval_seconds: The interval in seconds to wait between polls.

    Returns:
        A TranscriptionJobResult object containing the job status and transcript details.
    """
    transcribe_client = get_transcribe_client()
    s3_client = get_s3_client()

    while True:
        try:
            response = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
            print(f"Transcription job '{job_name}' status: {job_status}")

            if job_status == "COMPLETED":
                result = TranscriptionJobResult.from_get_transcription_job_response(
                    response
                )
                transcript_uri = result.transcript_uri

                if transcript_uri:
                    # Parse bucket and key from S3 URI
                    uri_parts = transcript_uri.replace("s3://", "").split("/", 1)
                    bucket_name = uri_parts[0]
                    key_name = uri_parts[1]

                    # Download transcript from S3
                    s3_object = s3_client.get_object(Bucket=bucket_name, Key=key_name)
                    transcript_content = s3_object["Body"].read().decode("utf-8")
                    transcript_json = json.loads(transcript_content)
                    result.parse_full_transcript_json(transcript_json)

                return result
            elif job_status == "FAILED":
                print(f"Transcription job '{job_name}' failed.")
                raise Exception(
                    f"Transcription job failed: {response['TranscriptionJob'].get('FailureReason', 'Unknown reason')}"
                )

            time.sleep(poll_interval_seconds)

        except Exception as e:
            print(f"Error polling transcription job: {e}")
            raise


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    JOB_NAME = os.environ.get("TRANSCRIPTION_JOB_NAME", "my-test-job-123")

    if "my-test-job-123" in JOB_NAME:
        print(
            "Please set TRANSCRIPTION_JOB_NAME environment variable or update script."
        )
    else:
        print(f"Polling transcription job '{JOB_NAME}'...")
        transcript_result = poll_transcription_job(job_name=JOB_NAME)
        print("Transcription job completed.")
        print("Full Transcript:")
        print(transcript_result.transcript_text)
        if transcript_result.diarized_segments:
            print("Diarized Segments:")
            for segment in transcript_result.diarized_segments:
                print(
                    f"  [Speaker {segment['speaker']} ({segment['start_time']:.2f}-{segment['end_time']:.2f}s)]: {segment['text']}"
                )
        if transcript_result.timestamped_words:
            print("Timestamped Words:")
            for word_info in transcript_result.timestamped_words:
                print(
                    f"  {word_info['word']} ({word_info['start_time']:.2f}-{word_info['end_time']:.2f}s)"
                )
