from google.cloud import speech
from speech_client import get_speech_client
from speech_models import SpeechConfig


def handle_streaming_responses(responses):
    """Processes streaming recognition responses, yielding partial and final transcripts."""
    print("Processing streaming responses...")
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            yield {"type": "final", "transcript": transcript}
        else:
            yield {"type": "partial", "transcript": transcript}
