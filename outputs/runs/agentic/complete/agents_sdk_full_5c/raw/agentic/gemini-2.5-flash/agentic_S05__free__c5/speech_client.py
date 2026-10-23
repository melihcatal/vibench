import os

from google.cloud import speech_v2

# Environment variable to specify the Google Cloud Project ID
# It's recommended to set this in your environment or Google Cloud SDK config.
# Example: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# Recognizer ID - You might create and configure a specific recognizer in GCP
# for your application, e.g., "my-app-recognizer"
# If not set, the default recognizer for the project and region will be used (if any).
RECOGNIZER_ID = os.getenv("SPEECH_RECOGNIZER_ID", "default-recognizer-id")

# Google Cloud Region for Speech-to-Text V2
# It's important to use a region that supports Speech V2 and where your recognizer is located.
LOCATION = os.getenv("SPEECH_LOCATION", "us-central1")

_speech_client = None

def get_speech_client() -> speech_v2.SpeechClient:
    """Returns a singleton Google Cloud Speech V2 client."""
    global _speech_client
    if _speech_client is None:
        if not PROJECT_ID:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or PROJECT_ID must be set.")
        _speech_client = speech_v2.SpeechClient(client_options={"api_endpoint": f"{LOCATION}-speech.googleapis.com"})
    return _speech_client

def get_project_resource_name() -> str:
    """Returns the full project resource name."""
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or PROJECT_ID must be set.")
    return f"projects/{PROJECT_ID}"

def get_recognizer_resource_name() -> str:
    """Returns the full recognizer resource name."""
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or PROJECT_ID must be set.")
    # For V2, the recognizer name format is projects/PROJECT_ID/locations/LOCATION/recognizers/RECOGNIZER_ID
    return f"projects/{PROJECT_ID}/locations/{LOCATION}/recognizers/{RECOGNIZER_ID}"


if __name__ == "__main__":
    # Example usage and verification
    print("--- Speech Client Helper --- ")
    try:
        # Set dummy project ID for testing if not set in env
        if "GOOGLE_CLOUD_PROJECT" not in os.environ:
            os.environ["GOOGLE_CLOUD_PROJECT"] = "your-test-project-id"
        if "SPEECH_RECOGNIZER_ID" not in os.environ:
            os.environ["SPEECH_RECOGNIZER_ID"] = "test-recognizer"
        if "SPEECH_LOCATION" not in os.environ:
            os.environ["SPEECH_LOCATION"] = "global"

        client = get_speech_client()
        print(f"Speech Client created: {client}")
        print(f"Project Resource Name: {get_project_resource_name()}")
        print(f"Recognizer Resource Name: {get_recognizer_resource_name()}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT environment variable is set.")

