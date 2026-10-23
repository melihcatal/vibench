import azure.cognitiveservices.speech as speechsdk
from queue import Queue
from threading import Thread

from speech_client import get_speech_config, get_push_audio_input_stream, get_speech_recognizer
from speech_models import normalize_azure_speech_result

def stream_with_language(payload, config=None):
    config = config or {}
    language_code = payload.get('language_code', "en-US")
    enable_punctuation = payload.get('enable_punctuation', False)

    speech_config = get_speech_config(api_key=config['api_key'],
                                      region=config['region'],
                                      language_code=language_code,
                                      enable_punctuation=enable_punctuation)
    
    stream = get_push_audio_input_stream(sample_rate_hz=payload.get('sample_rate_hz', 16000))
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    recognizer = get_speech_recognizer(speech_config=speech_config, audio_config=audio_config)
    
    events = Queue()
    recognizer.recognizing.connect(lambda e: events.put(normalize_azure_speech_result(e, is_final=False)))
    recognizer.recognized.connect(lambda e:
                                  events.put(normalize_azure_speech_result(e, is_final=True))
                                  if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None)
    recognizer.session_stopped.connect(lambda e: events.put(None))
    recognizer.canceled.connect(lambda e: events.put(RuntimeError(f'Azure speech recognition canceled: {e.reason}')))

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
