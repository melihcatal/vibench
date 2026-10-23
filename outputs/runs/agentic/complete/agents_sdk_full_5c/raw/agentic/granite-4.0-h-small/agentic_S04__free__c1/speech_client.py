import os
from typing import BinaryIO, Optional
from pydantic import BaseModel, Field
from azure.identity import DefaultAzureCredential
from azure.cognitiveservices.speech import SpeechConfig, AudioDataStream, SpeechRecognizer, SpeechSynthesizer

# ------------------------------------------------------------
# speech_client.py
# Local helper that configures and provides high‑level wrappers for Azure Batch STT
# ------------------------------------------------------------

class BatchSpeechClient:
    """Thin wrapper around Azure Speech Service REST API for batch transcription.

    The client uses the AZURE_SPEECH_API_KEY environment variable for authentication.
    """

    def __init__(self) -> None:
        # Retrieve API key from environment (fallback to placeholder for local testing)
        self.api_key = os.getenv("AZURE_SPEECH_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set AZURE_SPEECH_API_KEY environment variable.")

        # Construct HTTP‑based Speech Config (Azure SDK expects connection string)
        # For REST we simply build endpoint and key auth headers; the SDK is used for
        # convenience but all calls are HTTP‑POST to the Batch endpoint.
        endpoint = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
        self.token = self._get_access_token(self.api_key, endpoint)

    def _get_access_token(self, subscription_key: str, sts_endpoint: str) -> str:
        import requests
        headers = {
            "Ocp-Apim-Subscription-Key": subscription_key
        }
        resp = requests.post(sts_endpoint, headers=headers)
        resp.raise_for_status()
        return resp.text

    def submit_batch_transcription(
        self,
        audio_bytes: BinaryIO,
        content_type: str,
        language: str = "en-US",
        diarization_enabled: bool = False
    ) -> str:
        """Submit audio for batch transcription.

        Returns the JSON body of the immediate response containing job_id.
        """
        endpoint = "https://<region>.stt.speech.microsoft.com/speechtotext/v3.0/transcriptions"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": content_type,
            "Accept": "application/json"
        }
        # NOTE: Azure SDK has a higher‑level submit_batch_transcription method.
        # Here we manually post to the REST endpoint for illustration.
        import json, requests
        payload = {
            "name": "batch_job",
            "properties": {
                "diarizationEnabled": diarization_enabled
            },
            "contentUrl": f"{endpoint}/content",  # placeholder; real API requires multipart upload
            "locale": language
        }
        resp = requests.post(endpoint, headers=headers, data=payload)
        resp.raise_for_status()
        return resp.text

    def get_transcription_job(self, job_id: str) -> dict:
        """Poll a transcription job status.

        Returns parsed JSON response.
        """
        endpoint = f"https://<region>.stt.speech.microsoft.com/speechtotext/v3.0/transcriptions/{job_id}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        resp = requests.get(endpoint, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_transcription_results(self, job_id: str) -> dict:
        """Download the final transcript results.

        Returns parsed JSON response.
        """
        endpoint = f"https://<region>.stt.speech.microsoft.com/speechtotext/v3.0/transcriptions/{job_id}/results"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        resp = requests.get(endpoint, headers=headers)
        resp.raise_for_status()
        return resp.json()
