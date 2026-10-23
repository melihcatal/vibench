import time
import requests
from speech_client import SpeechClient
from speech_models import TranscriptionResult


def poll_transcription_job(
    job_name: str, wait_interval_seconds: int = 10
) -> TranscriptionResult:
    client = SpeechClient().get_client()

    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]

        if status == "COMPLETED":
            transcript_file_uri = response["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]
            transcript_content = requests.get(transcript_file_uri).json()
            full_transcript = " ".join(
                [
                    item["alternatives"][0]["content"]
                    for item in transcript_content["results"]["items"]
                    if "content" in item["alternatives"][0]
                ]
            )
            return TranscriptionResult(
                job_name=job_name, status=status, transcript=full_transcript
            )
        elif status == "FAILED":
            return TranscriptionResult(job_name=job_name, status=status)

        time.sleep(wait_interval_seconds)
