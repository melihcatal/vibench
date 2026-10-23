import os
import requests
import time
from speech_client import AzureSpeechClient
from speech_models import TranscriptionRequest, TranscriptionResponse

def submit_transcription(request: TranscriptionRequest) -> TranscriptionResponse:
    client = AzureSpeechClient()
    speech_config = client.get_speech_config()
    # In a real scenario, you would upload the audio file to Azure Blob Storage
    # and provide the URL to the Azure Speech-to-Text batch transcription API.
    # The batch transcription API is typically a REST API, not directly part of the SDK's SpeechRecognizer.
    # For demonstration, we'll simulate the submission and return a dummy job ID.

    # Example of how you might interact with Azure Storage to get a blob URL
    # blob_service_client = client.get_blob_service_client()
    # container_name = "audio-files"
    # blob_name = os.path.basename(request.audio_file_url)
    # blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    # # In a real scenario, you'd upload the file here or get a pre-signed URL
    # source_audio_url = blob_client.url # This would be the URL passed to the batch API
    
    # Simulating a call to the Azure Speech-to-Text batch transcription REST API
    # This URL is a placeholder and would need to be the actual Azure batch transcription endpoint
    # Documentation: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription-create
    
    # A realistic batch transcription API submission would look something like this (simplified):
    # headers = {
    #     "Ocp-Apim-Subscription-Key": client.speech_key,
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "contentUrls": [request.audio_file_url], # Assuming direct URL or SAS URL
    #     "properties": {
    #         "diarizationEnabled": request.diarization_enabled,
    #         "wordLevelTimestampsEnabled": request.word_timestamps_enabled
    #     },
    #     "locale": request.language,
    #     "displayName": f"Transcription for {os.path.basename(request.audio_file_url)}"
    # }
    # response = requests.post(f"https://{client.service_region}.customspeech.ai/api/speechtotext/v3.1/transcriptions", headers=headers, json=data)
    # response.raise_for_status()
    # job_id = response.json()["self"]

    # For this exercise, we'll return a mock job ID and status
    mock_job_id = f"job_{int(time.time())}"
    print(f"[MOCK] Submitted transcription job with ID: {mock_job_id} for {request.audio_file_url}")

    return TranscriptionResponse(
        job_id=mock_job_id,
        status="submitted",
    )
