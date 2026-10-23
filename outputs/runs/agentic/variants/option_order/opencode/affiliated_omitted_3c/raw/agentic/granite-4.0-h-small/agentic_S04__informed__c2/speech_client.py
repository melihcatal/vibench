# HELPER: speech_client.py

# Local configuration utilities for batch speech-to-text
# Uses environment variables for each supported provider.
import os


class SpeechConfig:
    """Centralized configuration for speech-to-text services."""

    # ----- AssemblyAI ----- (used by same-scenario files)
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

    # ----- Google Cloud ----- (used by diarized & timestamped helpers)
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )  # Path to JSON key file

    # ----- Amazon Transcribe ----- (used by timestamped helper)
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    @classmethod
    def is_valid(cls) -> bool:
        """Return True if at least one service configuration is present."""
        return any(
            [
                cls.ASSEMBLYAI_API_KEY,
                cls.GOOGLE_APPLICATION_CREDENTIALS,
                cls.AWS_ACCESS_KEY_ID and cls.AWS_SECRET_ACCESS_KEY,
            ]
        )
