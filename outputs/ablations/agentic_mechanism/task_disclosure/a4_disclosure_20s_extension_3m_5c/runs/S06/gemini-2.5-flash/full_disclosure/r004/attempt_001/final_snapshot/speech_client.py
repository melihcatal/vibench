import os
from google.cloud import texttospeech

class SpeechClient:
    def __init__(self):
        # Set up Google Cloud credentials from environment variable
        # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set
        # to the path of your service account key file.
        # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
            print("Please set it to the path of your Google Cloud service account key file.")
            # Depending on the use case, you might want to raise an exception here
            # raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set.")
        
        self.client = texttospeech.TextToSpeechClient()

    def get_client(self):
        return self.client

    # Add other client helper utilities as needed in the future
