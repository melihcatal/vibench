import time
from typing import Optional
from speech_client import SpeechClient
from speech_models import TranscriptSegment, TranscriptionJobResponse


def poll_transcription(
    job_name: str, max_attempts: int = 30, delay: int = 10
) -> Optional[str]:
    client = SpeechClient()
    for _ in range(max_attempts):
        try:
            response = client.client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]
            if status == "COMPLETED":
                transcript_uri = response["TranscriptionJob"]["Transcript"][
                    "TranscriptFileUri"
                ]
                import requests

                transcript_response = requests.get(transcript_uri)
                transcript_response.raise_for_status()
                transcript_data = transcript_response.json()
                return transcript_data["results"]["transcripts"][0]["transcript"]
            elif status == "FAILED":
                raise Exception(
                    f"Transcription job failed: {response['TranscriptionJob'].get('FailureReason', 'Unknown error')}"
                )
        except Exception as e:
            raise Exception(f"Failed to poll transcription job: {e}")
        time.sleep(delay)
    raise Exception("Transcription job polling timed out")
