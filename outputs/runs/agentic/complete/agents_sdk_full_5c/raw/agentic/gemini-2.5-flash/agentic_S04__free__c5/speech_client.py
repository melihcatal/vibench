from google.cloud import speech_v1p1beta1 as speech
import os

def get_speech_client():
    """Provides a configured Google Cloud Speech-to-Text client instance.

    Returns:
        A google.cloud.speech_v1p1beta1.SpeechClient instance.
    """
    # Credentials will be loaded automatically if running in GCP environment
    # or if GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return speech.SpeechClient()

def get_operations_client():
    """Provides a configured Google Cloud Operations client instance.

    Returns:
        A google.cloud.speech_v1p1beta1.SpeechClient.operations_client instance.
    """
    return speech.SpeechClient().operations_client

if __name__ == '__main__':
    # Example usage
    client = get_speech_client()
    print(f"SpeechClient instance created: {client}")
    ops_client = get_operations_client()
    print(f"OperationsClient instance created: {ops_client}")
