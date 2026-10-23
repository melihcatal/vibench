from google.cloud import speech_v1p1beta1 as speech


def handle_streaming_recognition_events(responses):
    """Iterates through responses and handles partial and final transcripts."""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            print(f"Final transcript: {transcript}")
            return transcript
        else:
            print(f"Partial transcript: {transcript}", end="\r")
            # For a real application, you might want to buffer or display partial results differently
    return None
