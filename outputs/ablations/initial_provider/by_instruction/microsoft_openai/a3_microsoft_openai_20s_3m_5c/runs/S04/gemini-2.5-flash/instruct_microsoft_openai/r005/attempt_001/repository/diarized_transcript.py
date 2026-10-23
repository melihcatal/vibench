import os
import requests
import json

def submit_diarization_job(audio_file_uri: str, locale: str = "en-US", speakers: int = 2):
    speech_key = os.environ.get("SPEECH_KEY")
    service_region = os.environ.get("SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables must be set.")

    base_url = f"https://{service_region}.api.cognitive.microsoft.com/speechtotext/v3.0"
    transcriptions_url = f"{base_url}/transcriptions"
    
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "application/json"
    }

    # Diarization settings are part of the properties for the transcription job
    payload = {
        "contentUrls": [audio_file_uri],
        "properties": {
            "diarizationEnabled": True,
            "diarization": {
                "speakers": {
                    "minCount": 1,
                    "maxCount": speakers
                }
            },
            "wordLevelTimestampsEnabled": True, # Often useful with diarization
        },
        "locale": locale,
        "displayName": f"Diarization Job for {os.path.basename(audio_file_uri)}"
    }

    print(f"Submitting diarization transcription job for {audio_file_uri}...")
    response = requests.post(transcriptions_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status() # Raise an exception for HTTP errors

    job_details = response.json()
    job_id = job_details.get("self").split("/")[-1] if job_details.get("self") else None

    if job_id:
        print(f"Diarization job submitted successfully. Job ID: {job_id}")
        print(f"Polling URL: {transcriptions_url}/{job_id}")
        return job_id
    else:
        print("Failed to retrieve job ID from the response.")
        return None

if __name__ == "__main__":
    # Example usage: Replace with a real audio file URI in Azure Blob Storage.
    # audio_blob_uri = "https://<your_storage_account>.blob.core.windows.net/<your_container>/<your_audio_file.wav>"
    # os.environ["SPEECH_KEY"] = "YOUR_AZURE_SPEECH_SERVICE_KEY"
    # os.environ["SPEECH_REGION"] = "YOUR_AZURE_SPEECH_SERVICE_REGION"

    # if "SPEECH_KEY" in os.environ and "SPEECH_REGION" in os.environ: # and audio_blob_uri != "https://<your_storage_account>.blob.core.windows.net/<your_container>/<your_audio_file.wav>":
    #     print(f"Attempting to submit diarization job for: {audio_blob_uri}")
    #     job_id = submit_diarization_job(audio_blob_uri, speakers=2)
    #     if job_id:
    #         print(f"Main function received job ID: {job_id}")
    #         print("You can use this job ID with poll_transcription.py to get the results.")
    # else:
    #     print("Please set SPEECH_KEY, SPEECH_REGION environment variables and provide a valid audio_blob_uri.")
    print("To run this example, set SPEECH_KEY, SPEECH_REGION environment variables and uncomment the test lines with a valid audio_blob_uri.")
