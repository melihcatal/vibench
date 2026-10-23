
from google.cloud import speech

def handle_streaming_recognition_response(response: speech.StreamingRecognizeResponse):
    """
    Handles a StreamingRecognizeResponse from Google Cloud Speech-to-Text,
    processing partial and final recognition results.
    """
    for result in response.results:
        if result.is_final:
            print(f"Final Transcript: {result.alternatives[0].transcript}")
        else:
            print(f"Partial Transcript: {result.alternatives[0].transcript}")

