import requests
import json
from speech_client import get_batch_transcription_client
from speech_models import TranscriptionRequest, TranscriptionResult

def submit_transcription_job(request: TranscriptionRequest) -> TranscriptionResult:
    client_config = get_batch_transcription_client()
    speech_key = client_config["key"]
    service_region = client_config["region"]
    endpoint = client_config["endpoint"]

    transcriptions_url = f"{endpoint}/transcriptions"

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "application/json"
    }

    payload = {
        "contentUrls": [
            request.audio_file_url
        ],
        "locale": request.locale,
        "displayName": request.display_name,
        "properties": {
            "wordLevelTimestampsEnabled": False,
            "diarizationEnabled": False,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked"
        }
    }

    try:
        response = requests.post(transcriptions_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors

        response_data = response.json()
        job_id = response_data.get("self") # The 'self' field usually contains the URL to the job status
        status = response_data.get("status")

        # Extracting the job ID from the 'self' URL
        job_id_extracted = job_id.split('/')[-1] if job_id else None

        return TranscriptionResult(
            id=job_id_extracted,
            status=status,
            transcript_url=job_id # The full URL to poll
        )
    except requests.exceptions.RequestException as e:
        print(f"Error submitting transcription job: {e}")
        return TranscriptionResult(
            id=None,
            status="Failed",
            error_message=str(e)
        )
