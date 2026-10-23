import os
from typing import Any, Dict

# Example: using AssemblyAI SDK (pip install assemblyai) for batch transcription
try:
    from assemblyai import AssemblyAI
    # If using Google Speech-to-Text SDK, replace with google-cloud-speech import
except ImportError:
    raise ImportError("Please install the required SDK, e.g., 'pip install assemblyai' for AssemblyAI.")


class SpeechClient:
    DEFAULT_HOST = "api.assemblyai.com"
    DEFAULT_ENDPOINT = "/v2/transcript"

    def __init__(self, api_key: str | None = None):
        # Load API key from env if not provided
        self.api_key: str = api_key or os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("AssemblyAI API key not found in environment or argument.")
        self.client = AssemblyAI(self.api_key)

    def transcribe(
        self,
        audio_path: str,
        speaker_diarization: bool = False,
        timestamps: bool = False,
        **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Submit transcript request
        payload: Dict[str, Any] = {"audio_url": self.upload_audio(audio_path)}
        if speaker_diarization:
            payload["diarization"] = "on"
        if timestamps:
            payload["timestamps"] = "true"
        # Add any additional provider-specific params via **kwargs
        response = self.client.submit_transcription(payload)
        return response  # should contain job_id/status fields

    def check_status(self, job_id: str) -> Dict[str, Any]:
        return self.client.get_transcript_status(job_id)

    def download_result(self, job_id: str) -> Dict[str, Any]:
        return self.client.get_transcript(job_id)

    def upload_audio(self, file_path: str) -> str:
        # Using the SDK's upload helper (auto-uploads to provider storage)
        with open(file_path, "rb") as f:
            return self.client.upload(f)

    def __repr__(self) -> str:
        return f"SpeechClient(provider=AssemblyAI)"

# End of file
