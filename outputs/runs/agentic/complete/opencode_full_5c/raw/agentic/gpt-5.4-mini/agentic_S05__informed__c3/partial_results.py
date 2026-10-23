import azure.cognitiveservices.speech as speechsdk

from speech_models import StreamingTranscriptEvent, normalize_transcript


def handle_partial_results(recognizer: speechsdk.SpeechRecognizer):
    events = []

    def on_recognizing(evt):
        events.append(
            StreamingTranscriptEvent(
                text=normalize_transcript(evt.result.text), is_final=False
            )
        )

    def on_recognized(evt):
        events.append(
            StreamingTranscriptEvent(
                text=normalize_transcript(evt.result.text), is_final=True
            )
        )

    recognizer.recognizing.connect(on_recognizing)
    recognizer.recognized.connect(on_recognized)
    return events
