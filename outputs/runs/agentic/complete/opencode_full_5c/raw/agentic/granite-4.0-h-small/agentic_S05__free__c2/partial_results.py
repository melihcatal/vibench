# [SAME-SCENARIO] partial_results.py

from google.cloud import speech_v1p1beta1 as speech

# Identify provider: Google Cloud Speech-to-Text


def handle_recognition_event(event):
    if (
        event.speech_event_type
        == speech.StreamingRecognitionEvent.SpeechEventType.INCREMENTAL
    ):
        return event.result.alternatives[0].transcript  # interim result
    else:  # FINAL
        return event.result.alternatives[0].transcript  # final result
