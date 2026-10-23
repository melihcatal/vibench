import requests
import os
import json
from speech_client import get_speech_config
from speech_models import TranscriptionRequest, TranscriptionJob

def submit_transcription(request: TranscriptionRequest) -> TranscriptionJob:
    speech_key, speech_region = get_speech_config()
    
    base_url = f"https://{speech_region}.api.cognitive.microsoft.com/speechtotext/v3.1"
    transcriptions_url = f"{base_url}/transcriptions"

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "application/json"
    }

    payload = {
        "contentUrls": [request.audio_file_url],
        "properties": {
            "diarizationEnabled": False,
            "wordLevelTimestampsEnabled": False,
            "punctuationsMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked",
            "languageIdentification": {
                "candidateLocales": [request.locale]
            }
        },
        "locale": request.locale,
        "displayName": request.display_name
    }
    
    if request.model_id:
        payload["model"] = {"self": f"{base_url}/models/{request.model_id}"}

    response = requests.post(transcriptions_url, headers=headers, json=payload)
    response.raise_for_status() 

    job_details = response.json()
    return TranscriptionJob(
        job_id=job_details["self"].split("/")[-1],
        status=job_details["status"],
        created_date_time=job_details["createdDateTime"],
        last_action_date_time=job_details["lastActionDateTime"],
        output_location=job_details.get("links", {}).get("files")
    )
