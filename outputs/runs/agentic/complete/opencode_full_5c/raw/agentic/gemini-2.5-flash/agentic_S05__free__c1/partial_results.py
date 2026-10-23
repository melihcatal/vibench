from google.cloud import speech_v1p1beta1 as speech


def handle_streaming_recognition_event(response: speech.StreamingRecognizeResponse):
    if not response.results:
        return None, None

    for result in response.results:
        if result.is_final:
            if result.alternatives:
                return result.alternatives[0].transcript, True
        else:
            if result.alternatives:
                # Interim transcript, often with a stability score
                return result.alternatives[0].transcript, False
    return None, None
