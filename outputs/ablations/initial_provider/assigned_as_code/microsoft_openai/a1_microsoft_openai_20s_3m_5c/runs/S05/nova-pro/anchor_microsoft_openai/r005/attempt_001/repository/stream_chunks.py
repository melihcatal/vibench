from queue import Queue
from threading import Thread
import azure.cognitiveservices.speech as speechsdk


def stream_chunks(payload, config=None):
    config = config or {}
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    speech_config.speech_recognition_language = payload['language_code']
    stream = speechsdk.audio.PushAudioInputStream(stream_format=speechsdk.audio.AudioStreamFormat(
        samples_per_second=payload['sample_rate_hz'], bits_per_sample=16, channels=1))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
        audio_config=speechsdk.audio.AudioConfig(stream=stream))
    events = Queue()
    recognizer.recognizing.connect(lambda e: events.put({'text': e.result.text, 'is_final': False}))
    recognizer.recognized.connect(lambda e: events.put({'text': e.result.text, 'is_final': True})
                                  if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None)
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