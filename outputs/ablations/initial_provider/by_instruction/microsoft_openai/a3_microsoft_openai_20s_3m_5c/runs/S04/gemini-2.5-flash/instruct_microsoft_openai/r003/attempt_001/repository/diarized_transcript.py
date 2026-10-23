import os
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

def submit_diarized_transcription(audio_file_path: str):
    """
    Submits an audio file for batch transcription with speaker diarization using Azure Speech-to-Text.
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
            "diarizationEnabled": True,  # Enable diarization
            "wordLevelTimestampsEnabled": False,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked"
        },
        "locale": "en-US",
        "displayName": "DiarizedBatchTranscriptionExample"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting diarized transcription: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with a valid audio file URL)
    # audio_url = "YOUR_AUDIO_FILE_URL_HERE"
    # diarization_job = submit_diarized_transcription(audio_url)
    # if diarization_job:
    #     print("Diarized transcription job submitted successfully:")
    #     print(f"  ID: {diarization_job.get('self')}")
    #     print(f"  Status: {diarization_job.get('status')}")
    #     print("Use poll_transcription.py with this ID to get results.")
    # else:
    #     print("Failed to submit diarized transcription job.")
    pass
