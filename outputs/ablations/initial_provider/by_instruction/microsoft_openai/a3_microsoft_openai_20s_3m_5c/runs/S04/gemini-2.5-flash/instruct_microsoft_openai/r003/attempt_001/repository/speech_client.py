import os
import requests
from dotenv import load_dotenv

class SpeechClient:
    """
    A client for interacting with the Azure Speech-to-Text API.
    """
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AZURE_SPEECH_KEY")
        self.region = os.getenv("AZURE_SPEECH_REGION")

        if not self.api_key or not self.region:
            raise ValueError("Azure Speech key and region must be set in environment variables.")

        self.base_url = f"https://{self.region}.api.cognitive.microsoft.com/speechtotext/v3.1"
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def submit_transcription_job(self, audio_file_url: str, diarization_enabled: bool = False, 
                                 word_level_timestamps_enabled: bool = False, display_name: str = "BatchTranscriptionJob"):
        """
        Submits an audio file for batch transcription.
        """
        url = f"{self.base_url}/transcriptions"
        payload = {
            "contentUrls": [audio_file_url],
            "properties": {
                "diarizationEnabled": diarization_enabled,
                "wordLevelTimestampsEnabled": word_level_timestamps_enabled,
                "punctuationMode": "DictatedAndAutomatic",
                "profanityFilterMode": "Masked"
            },
            "locale": "en-US",
            "displayName": display_name
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error submitting transcription job: {e}")
            return None

    def get_transcription_status(self, transcription_id: str):
        """
        Gets the status of a transcription job.
        """
        url = f"{self.base_url}/transcriptions/{transcription_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting transcription status: {e}")
            return None

    def get_transcription_results(self, files_url: str):
        """
        Gets the results of a completed transcription job.
        """
        try:
            response = requests.get(files_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting transcription results: {e}")
            return None

    def get_transcript_content(self, content_url: str):
        """
        Gets the actual transcript content from a content URL.
        """
        try:
            response = requests.get(content_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting transcript content: {e}")
            return None
