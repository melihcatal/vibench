import os
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

def submit_transcription(audio_file_path: str):
    """
    Submits an audio file for batch transcription using Azure Speech-to-Text.
    """
    if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION:
        raise ValueError("Azure Speech key and region must be set in environment variables.")

    url = f"https://{AZURE_SPEECH_REGION}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "contentUrls": [audio_file_path],
        "properties": {
            "diarizationEnabled": False,
            "wordLevelTimestampsEnabled": False,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked"
        },
        "locale": "en-US",
        "displayName": "BatchTranscriptionExample"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting transcription: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with a valid audio file URL)
    audio_url = "YOUR_AUDIO_FILE_URL_HERE"
    
    # For local files, you would need to upload them to a blob storage first and provide the SAS URL.
    # This example assumes a publicly accessible audio file URL or a SAS URL from Azure Blob Storage.
    
    # To run this example:
    # 1. Create a .env file in the same directory with your AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.
    # 2. Replace "YOUR_AUDIO_FILE_URL_HERE" with an actual URL to an audio file.
    
    # Example for a local file (requires Azure Blob Storage upload first):
    # from azure.storage.blob import BlobServiceClient
    # blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    # blob_client = blob_service_client.get_blob_client(container="your_container", blob="your_audio.wav")
    # with open("path/to/your_audio.wav", "rb") as data:
    #     blob_client.upload_blob(data)
    # audio_url = blob_client.url # You might need to generate a SAS token for public access.
    
    # transcription_job = submit_transcription(audio_url)
    # if transcription_job:
    #     print("Transcription job submitted successfully:")
    #     print(f"  ID: {transcription_job.get('self')}")
    #     print(f"  Status: {transcription_job.get('status')}")
    # else:
    #     print("Failed to submit transcription job.")
