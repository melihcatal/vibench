from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk


def normalize_result(result):
    return {'text': result.text, 'is_final': result.is_final}


def handle_events(recognizer):
    events = Queue()
    recognizer.recognizing.connect(lambda e: events.put(normalize_result(e.result)))
    recognizer.recognized.connect(lambda e: events.put(normalize_result(e.result))
                                  if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None)
    recognizer.session_stopped.connect(lambda e: events.put(None))
    recognizer.canceled.connect(lambda e: events.put(RuntimeError('Azure speech recognition canceled')))
    return events