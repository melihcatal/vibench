# Amazon Transcribe integration with timestamped output
import os
import boto3
import json
from submit_transcription import submit_transcription

TRANSCRIBE = boto3.client(
    "transcribe",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def get_timestamped_transcript(job_name, poll_interval=10):
    """Poll a transcription job and return a list of segment objects with start and end times.
    TranscribeSegmentFormat must be enabled in the job settings for this to work.
    Returns JSON list of segments.
    """
    # Start transcription job with timestamps enabled (TranscriptionJobName will be reused)
    submit_transcription(
        job_name, "s3://my-bucket/audio.mp3"
    )  # placeholder audio, job already submitted

    while True:
        response = TRANSCRIBE.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            results_uri = response["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]
            # Download results file (assumes small size)
            import urllib.request, tempfile

            with tempfile.NamedTemporaryFile() as tmp:
                urllib.request.urlretrieve(results_uri, tmp.name)
                with open(tmp.name, "r") as f:
                    data = json.load(f)
                    segments = []
                    for result in data["results"]["items"]:
                        if result["type"] == "pronunciation":  # or segment objects
                            start = result.get("start_time")
                            end = result.get("end_time")
                            segment = {
                                "start": start,
                                "end": end,
                                "text": result["alternatives"][0]["content"],
                            }
                            segments.append(segment)
                    return segments
        elif status == "FAILED":
            raise RuntimeError(
                f"Transcription job failed: {response['TranscriptionJob']['FailureReason']}"
            )
        print(f"Job status: {status}. Waiting {poll_interval}s...")
        time.sleep(poll_interval)
