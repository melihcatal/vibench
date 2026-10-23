import os
import json


# Local helper: configuration loading and client utilities for Batch Speech-to-Text
class SpeechClient:
    """Helper client that abstracts provider-specific SDKs and auth."""

    def __init__(self):
        # Load environment variables for the chosen provider (example: Watson STT)
        self.api_key = os.getenv("IBM_STT_APIKEY")
        self.url = os.getenv("IBM_STT_URL")
        # Initialize provider SDK (import inside to avoid early errors if not installed)
        from ibm_watson import SpeechToTextV1

        self.stt = SpeechToTextV1(authenticator=APIKeyAuthenticator(self.api_key))
        self.stt.set_service_url(self.url)

    def create_batch_transcription_request(self, audio_path):
        """Build payload for batch transcription request."""
        with open(audio_path, "rb") as f:
            audio = f.read()
        return {
            "audio": audio,
            "content_type": "audio/wav",
            "model": "en-US_BroadbandModel",
        }

    def create_diarized_request(self, audio_path, speaker_count=2):
        with open(audio_path, "rb") as f:
            audio = f.read()
        return {
            "audio": audio,
            "content_type": "audio/wav",
            "model": "en-US_BroadbandModel",
            "diarization": {
                "enabled": True,
                "speaker_count": speaker_count,
            },
        }

    def submit_batch(self, payload):
        """Submit batch job to provider and return JSON response."""
        return self.stt.recognize_batch(payload).get_result()

    def poll_batch(self, job_id):
        """Poll the status of a batch job."""
        return self.stt.check_job(job_id).get_result()

    def get_transcription_with_timestamps(self, job_id):
        """Retrieve transcript with word/segment timestamps."""
        return self.stt.get_job_result(job_id).get_result()
