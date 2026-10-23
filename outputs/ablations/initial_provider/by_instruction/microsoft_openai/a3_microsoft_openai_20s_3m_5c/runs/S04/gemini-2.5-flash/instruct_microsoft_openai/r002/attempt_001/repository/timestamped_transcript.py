import requests
import json
from speech_client import get_speech_config
from speech_models import TranscriptionRequest, TranscriptionJob, TranscriptionResult
from submit_transcription import submit_transcription
from poll_transcription import poll_transcription

def request_timestamped_transcript(audio_file_url: str, locale: str = "en-US", display_name: str = "TimestampedTranscriptionJob") -> TranscriptionResult:
    speech_key, speech_region = get_speech_config()
    
    base_url = f"https://{speech_region}.api.cognitive.microsoft.com/speechtotext/v3.1"
    transcriptions_url = f"{base_url}/transcriptions"

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "application/json"
    }

    payload = {
        "contentUrls": [audio_file_url],
        "properties": {
            "wordLevelTimestampsEnabled": True,
            "punctuationsMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked",
            "languageIdentification": {
                "candidateLocales": [locale]
            }
        },
        "locale": locale,
        "displayName": display_name
    }
    
    response = requests.post(transcriptions_url, headers=headers, json=payload)
    response.raise_for_status() 

    job_details = response.json()
    job = TranscriptionJob(
        job_id=job_details["self"].split("/")[-1],
        status=job_details["status"],
        created_date_time=job_details["createdDateTime"],
        last_action_date_time=job_details["lastActionDateTime"],
        output_location=job_details.get("links", {}).get("files")
    )

    return poll_transcription(job)
