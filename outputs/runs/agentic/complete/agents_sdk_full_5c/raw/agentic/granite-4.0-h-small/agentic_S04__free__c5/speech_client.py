import os
from typing import Any, Dict

# Example provider: Google Cloud Speech-to-Text (client library name "google-cloud-speech")
# The client class name reflects the provider (google.cloud.speech_v1p1beta1.services.speech.SpeechClient)
try:
    from google.cloud import speech_v1p1beta1 as speech
except ImportError:
    raise RuntimeError('Google Cloud Speech client library not installed. Run `pip install google-cloud-speech`')

class BatchSpeechClient:
    """Lightweight wrapper around the provider's speech client for batch jobs."""
    def __init__(self):
        # Credentials are pulled from GOOGLE_APPLICATION_CREDENTIALS env var or default application default credentials
        self.client = speech.SpeechClient()

    def create_transcription_job(
        self,
        request: Any,
        location: str = None,
        project: str = None,
    ) -> Any:
        """Submit a batch transcription job. The underlying provider method name is `create_custom_job` for speech batch.",
        # The real API call will look like:
        # self.client.projects_locations_custom_jobs.CreateCustomJob(parent=f'projects/{project}/locations/{location}', request=request)
        # Here we just adapt the generic method name for the wrapper.
        return self.client.create_custom_job(
            request=request,
            location=location or os.getenv('BATCH_SPEECH_LOCATION', 'us-central1'),
            parent=f"projects/{project}/locations/{location or os.getenv('BATCH_SPEECH_LOCATION', 'us-central1')})"
        )

    def get_transcription_job_status(self, job_id: str) -> str:
        # Provider call: projects_locations_custom_jobs.GetCustomJob(name=f'projects/{project}/locations/{location}/jobs/{job_id}')
        return self.client.get_custom_job(name=job_id).state  # mock state property

    def get_transcription_job_result(self, job_id: str) -> Dict[str, Any]:
        # Pull the response protobuf, convert to dict for downstream helpers
        response = self.client.get_custom_job(name=job_id).response  # mock
        return response.to_dict()  # simplify for local helpers
