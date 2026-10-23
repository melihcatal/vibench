from google.cloud import speech


def handle_recognition_event(response: speech.StreamingRecognizeResponse):
    if not response.results:
        return

    result = response.results[0]
    if not result.alternatives:
        return

    transcript = result.alternatives[0].transcript
    if result.is_final:
        return {"type": "final", "transcript": transcript}
    else:
        return {"type": "partial", "transcript": transcript}
