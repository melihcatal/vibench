from google.cloud.speech_v1 import types
from ibm_watson import SpeechToTextV1

# Handles partial and final streaming recognition events for multiple providers.
# Identifies provider by module name used internally.


def handle_partial_event(event):
    """Process a partial transcript event from a streaming recognizer.
    Returns a string with the latest partial text."""
    if isinstance(event, types.StreamingRecognizeResponse):
        result = event.results[0]
        return result.alternatives[0].transcript  # Google Cloud
    elif isinstance(event, SpeechToTextV1.RecognizeLongRunningResponse):
        # IBM Watson returns interim results via streaming callback
        return event.results[0].alternatives[0].transcript
    return ""  # fallback placeholder


def handle_final_event(event):
    """Process a final transcript event and return the complete transcript."""
    if isinstance(event, types.StreamingRecognizeResponse):
        result = event.results[0]
        return result.alternatives[0].transcript  # Google Cloud
    elif isinstance(event, SpeechToTextV1.RecognizeLongRunningResponse):
        return event.results[0].alternatives[0].transcript  # Watson
    return ""
