import requests
import time
from speech_client import get_batch_transcription_client
from speech_models import TranscriptionResult

def poll_transcription_job(job_url: str) -> TranscriptionResult:
    client_config = get_batch_transcription_client()
    speech_key = client_config["key"]

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
    }

    while True:
        try:
            response = requests.get(job_url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            status = response_data.get("status")
            job_id = response_data.get("id") # The 'id' field should contain the job ID

            if status == "Succeeded":
                # Get the results URL
                files_url = response_data["links"]["files"]
                files_response = requests.get(files_url, headers=headers)
                files_response.raise_for_status()
                files_data = files_response.json()

                transcript_url = None
                for file_entry in files_data["values"]:
                    if file_entry["kind"] == "Transcription":
                        transcript_url = file_entry["links"]["contentUrl"]
                        break

                return TranscriptionResult(
                    id=job_id,
                    status=status,
                    transcript_url=transcript_url
                )
            elif status in ["Failed", "Canceled"]:
                error_message = response_data.get("properties", {}).get("error", {}).get("message")
                return TranscriptionResult(
                    id=job_id,
                    status=status,
                    error_message=error_message or "Transcription job failed or was canceled."
                )
            else:
                print(f"Transcription job {job_id} is in status: {status}. Waiting...")
                time.sleep(30)  # Wait for 30 seconds before polling again

        except requests.exceptions.RequestException as e:
            print(f"Error polling transcription job: {e}")
            return TranscriptionResult(
                id=None,
                status="Failed",
                error_message=str(e)
            )
