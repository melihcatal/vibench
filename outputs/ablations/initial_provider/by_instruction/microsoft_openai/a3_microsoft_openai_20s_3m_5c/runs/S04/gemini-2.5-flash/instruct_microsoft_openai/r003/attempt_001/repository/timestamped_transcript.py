import os
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

def submit_timestamped_transcription(audio_file_path: str):
    """
    Submits an audio file for batch transcription with word-level timestamps using Azure Speech-to-Text.
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
            "wordLevelTimestampsEnabled": True,  # Enable word-level timestamps
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked"
        },
        "locale": "en-US",
        "displayName": "TimestampedBatchTranscriptionExample"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting timestamped transcription: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with a valid audio file URL)
    # audio_url = "YOUR_AUDIO_FILE_URL_HERE"
    # timestamped_job = submit_timestamped_transcription(audio_url)
    # if timestamped_job:
    #     print("Timestamped transcription job submitted successfully:")
    #     print(f"  ID: {timestamped_job.get('self')}")
    #     print(f"  Status: {timestamped_job.get('status')}")
    #     print("Use poll_transcription.py with this ID to get results.")
    # else:
    #     print("Failed to submit timestamped transcription job.")
    pass
