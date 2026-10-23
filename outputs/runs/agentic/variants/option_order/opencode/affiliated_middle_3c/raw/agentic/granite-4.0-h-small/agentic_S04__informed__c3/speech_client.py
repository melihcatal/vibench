import os
import boto3
from botocore.config import Config


def get_speech_client(provider="boto3"):
    """Return a configured client for batch transcription based on the selected provider.

    Parameters
    ----------
    provider : str, optional
        Provider name. Currently supports 'boto3' for Amazon Transcribe (default).

    Returns
    -------
    botocore.client.TranscribeService
        Configured client ready to call AWS Transcribe APIs.
    """
    if provider == "boto3":
        # Basic boto3 Transcribe client with retries and timeout
        return boto3.client(
            "transcribe", config=Config(retries={"max_attempts": 5, "mode": "standard"})
        )
    raise NotImplementedError(f"Provider {provider} not implemented in speech_client")
