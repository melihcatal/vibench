import os
from google.cloud import texttospeech

def get_tts_client():
    """Returns an initialized Google Cloud Text-to-Speech client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # to the path of your service account key file.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    try:
        client = texttospeech.TextToSpeechClient()
        print("Google Cloud Text-to-Speech client initialized.")
        return client
    except Exception as e:
        print(f"Error initializing Google Cloud Text-to-Speech client: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # client = get_tts_client()
    # if client:
    #     print("Client obtained successfully.")
    # else:
    #     print("Failed to obtain client.")
    pass
