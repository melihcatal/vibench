import os

# provider: Azure Speech Service
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_SPEECH_ENDPOINT")

import http.client
import json


class SpeechClient:
    """
    Simple client wrapper for Azure Speech-to-Text batch endpoint.
    """

    def __init__(self):
        self.conn = http.client.HTTPSConnection(AZURE_ENDPOINT)
        self.headers = {
            "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
            "Content-Type": "application/json",
        }

    def submit_job(self, audio_blob, language="en-US", model="default"):
        """Submit an audio blob (base64) for batch transcription."""
        payload = {
            "ContentUrl": f"{AZURE_ENDPOINT}/audio/{audio_blob}",
            "ContentLanguage": language,
            "Properties": {"Model": model},
        }
        self.conn.request(
            "POST",
            "/speechtotext/v3.0/transcriptions",
            json.dumps(payload),
            self.headers,
        )
        response = self.conn.getresponse()
        response.raise_for_status()
        result = json.load(response)
        return result["properties"]["statusUri"]  # e.g., URL to poll status

    def poll_job(self, status_uri):
        """Poll until the transcription completes."""
        while True:
            self.conn.request("GET", status_uri, headers=self.headers)
            response = self.conn.getresponse()
            response.raise_for_status()
            job = json.load(response)
            status = job["properties"]["status"]
            if status == "SUCCEEDED":
                return job["properties"]["resultUri"]  # URL to retrieve transcript
            elif status == "FAILED":
                raise RuntimeError(
                    f"Transcription failed: {job['properties'].get('error')}"
                )
            time.sleep(10)

    def retrieve_transcript(self, result_uri):
        """Download the completed transcript JSON."""
        self.conn.request("GET", result_uri, headers=self.headers)
        response = self.conn.getresponse()
        response.raise_for_status()
        return json.load(response)
