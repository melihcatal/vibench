# [HELPER] speech_client.py
import os
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# ------------------------------------------------------------------------------
# Configuration (read from environment variables for security)
# ------------------------------------------------------------------------------
IBM_STT_URL = os.getenv("IBM_STT_URL", "https://api.us-south.speech-to-text.watson.cloud.ibm.com")
IBM_STT_APIKEY = os.getenv("IBM_STT_APIKEY")

if not IBM_STT_APIKEY:
    raise RuntimeError("Set the environment variable IBM_STT_APIKEY with your IBM Watson Speech-to-Text API key.")

# ------------------------------------------------------------------------------
# Helper class for batch speech-to-text operations
# ------------------------------------------------------------------------------
class BatchSpeechClient:
    """Thin wrapper around IBM Watson Speech-to-Text SDK supporting batch jobs."""
    def __init__(self):
        self.authenticator = IAMAuthenticator(IBM_STT_APIKEY)
        self.service = SpeechToTextV1(authenticator=self.authenticator)
        self.service.set_service_url(IBM_STT_URL)

    def submit_batch_transcription(self,
                                    audio_path: str,
                                    language: str = "en-US",
                                    diarization_config: dict = None,
                                    timestamping: bool = False) -> dict:
        """Submit a batch job and return the generated job_id.

        Args:
            audio_path (str): Local path to audio file.
            language (str): BCP-47 language code (default 'en-US').
            diarization_config (dict): Optional dict with 'speaker_count' and 'enable'.
            timestamping (bool): Whether to request word timestamps.

        Returns:
            dict: JSON response containing 'jobId'.
        """
        with open(audio_path, 'rb') as audio_file:
            params = {
                'audio': audio_file,
                'content_type': 'audio/wav',
                'model': language,
                'timestamps': timestamping
            }
            if diarization_config:
                params['diarization'] = diarization_config
                # Watson uses 'speaker_labels' param for diarization
                params['speaker_labels'] = {'enabled': True}
            response = self.service.recognize_using_websocket(
                audio=audio_file,
                content_type='audio/wav',
                model=language,
                timestamps=timestamping,
                diarization=diarization_config
            ).get_result()
            # The real SDK uses websocket; for batch we simulate sync via recognize
            # Here we call the HTTP recognize endpoint for demo purposes
            recognize_response = self.service.recognize(
                audio=audio_file,
                content_type='audio/wav',
                model=language,
                timestamps=timestamping,
                speaker_labels=diarization_config["enabled"] if diarization_config else None
            ).get_result()
            # In production, you would use the asynchronous job APIs instead
            return {
                "job_id": "simulated-job-id-123",
                "status": "completed",
                "result": recognize_response.get('results', [])
            }

    def get_job_status(self, job_id: str) -> str:
        """Poll the job status. (Placeholder for real async API.)"""
        return "completed"

    def get_transcription_result(self, job_id: str) -> dict:
        """Retrieve transcription result for a completed job. (Placeholder.)"""
        return {
            "results": [
                {
                    "alternatives": [
                        {
                            "transcript": "This is a sample transcription.",
                            "timestamps": []
                        }
                    ]
                }
            ]
        }

# ------------------------------------------------------------------------------
# Export simplified functions for the same-scenario scripts
# ------------------------------------------------------------------------------
def submit_batch_transcription(*args, **kwargs):
    return BatchSpeechClient().submit_batch_transcription(*args, **kwargs)

def get_job_status(*args, **kwargs):
    return BatchSpeechClient().get_job_status(*args, **kwargs)

def get_transcription_result(*args, **kwargs):
    return BatchSpeechClient().get_transcription_result(*args, **kwargs)
