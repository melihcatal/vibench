from queue import Queue
from threading import Thread

import azure.cognitiveservices.speech as speechsdk

from speech_client import build_push_stream, build_speech_config
from speech_models import normalize_transcript_event


def partial_results(payload, config=None):
    speech_config = build_speech_config(config)
    speech_config.speech_recognition_language = payload['language_code']
    stream = build_push_stream(payload['sample_rate_hz'])
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=speechsdk.audio.AudioConfig(stream=stream))
    events = Queue()
    recognizer.recognizing.connect(lambda e: events.put(normalize_transcript_event(e.result.text, False, offset=e.result.offset)))
    recognizer.recognized.connect(lambda e: events.put(normalize_transcript_event(e.result.text, True, offset=e.result.offset)) if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None)
    recognizer.session_stopped.connect(lambda e: events.put(None))
    recognizer.canceled.connect(lambda e: events.put(RuntimeError('Azure speech recognition canceled')))

    def feed():
        try:
            for chunk in payload['audio_chunks']:
                stream.write(chunk)
        except Exception as exc:
            events.put(exc)
        finally:
            stream.close()

    recognizer.start_continuous_recognition_async().get()
    producer = Thread(target=feed, daemon=True)
    producer.start()
    try:
        while True:
            event = events.get(timeout=60)
            if event is None:
                break
            if isinstance(event, Exception):
                raise event
            yield event
    finally:
        recognizer.stop_continuous_recognition_async().get()
        stream.close()
        producer.join(timeout=1)
