import os
import assemblyai as aai


class SpeechClient:
    """
    Local helper providing configuration and client utilities for IBM Watson Speech-to-Text.
    """

    def __init__(self):
        self.api_key = os.getenv("IBM_STT_APIKEY")
        self.service_url = os.getenv("IBM_STT_URL")
        if not self.api_key or not self.service_url:
            raise RuntimeError(
                "IBM_STT_APIKEY and IBM_STT_URL must be set in environment variables"
            )
        self.client = aai.WatsonTranscriber(
            api_key=self.api_key, service_url=self.service_url
        )

    def transcribe_file(self, audio_path: str) -> str:
        """Submit a monolithic transcription job and return the job UUID."""
        return self.client.transcribe(audio_path).id

    def check_job(self, job_id: str) -> aai.Transcript:
        """Poll a transcription job until it completes."""
        while True:
            transcript = self.client.get_transcript(job_id)
            if transcript.status == "completed":
                return transcript
            if transcript.status == "errored":
                raise RuntimeError(f"Transcription error: {transcript.error}")
            time.sleep(5)
