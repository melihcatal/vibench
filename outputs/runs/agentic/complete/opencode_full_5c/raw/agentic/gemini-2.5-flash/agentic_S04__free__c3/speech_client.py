from google.cloud import speech_v1p1beta1 as speech
import os


def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # default credentials are available.
    return speech.SpeechClient()


def get_project_id():
    """Returns the Google Cloud project ID from the environment."""
    # This is a placeholder. In a real scenario, you might get this from
    # google.auth.default() or a config file.
    return os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-google-cloud-project-id")
