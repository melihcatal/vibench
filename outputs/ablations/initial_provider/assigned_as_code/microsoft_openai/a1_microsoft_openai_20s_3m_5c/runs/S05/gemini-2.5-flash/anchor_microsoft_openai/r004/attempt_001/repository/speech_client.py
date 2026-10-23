import azure.cognitiveservices.speech as speechsdk
from speech_models import StreamingRecognitionConfig, SpeechRecognitionResult, normalize_azure_result
from queue import Queue
from threading import Thread
from typing import Dict, Any, Generator, Optional

class AzureSpeechClient:
    def __init__(self, api_key: str, region: str):
        self.speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

    def stream_recognize(self, audio_chunks: Generator[bytes, None, None], config: StreamingRecognitionConfig) -> Generator[SpeechRecognitionResult, None, None]:
        self.speech_config.speech_recognition_language = config.language_code
        if config.enable_automatic_punctuation:
            self.speech_config.set_service_property("punctuation", "true", speechsdk.ServicePropertyChannel.UriQueryParameter)

        stream = speechsdk.audio.PushAudioInputStream(speechsdk.audio.AudioStreamFormat(
            samples_per_second=config.sample_rate_hz, bits_per_sample=16, channels=1))
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        events = Queue()

        def recognizing_handler(e):
            if e.result.text:
                events.put({'text': e.result.text, 'is_final': False})

        def recognized_handler(e):
            if e.result.reason == speechsdk.ResultReason.RecognizedSpeech and e.result.text:
                events.put({'text': e.result.text, 'is_final': True})
            elif e.result.reason == speechsdk.ResultReason.NoMatch:
                # Handle no match case, perhaps log it or send an empty result
                pass

        def session_stopped_handler(e):
            events.put(None)

        def canceled_handler(e):
            events.put(RuntimeError(f'Azure speech recognition canceled: {e.cancellation_details.reason} - {e.cancellation_details.error_details}'))

        recognizer.recognizing.connect(recognizing_handler)
        recognizer.recognized.connect(recognized_handler)
        recognizer.session_stopped.connect(session_stopped_handler)
        recognizer.canceled.connect(canceled_handler)

        def feed_audio():
            try:
                for chunk in audio_chunks:
                    stream.write(chunk)
            except Exception as exc:
                events.put(exc)
            finally:
                stream.close()

        recognizer.start_continuous_recognition_async().get()
        producer = Thread(target=feed_audio, daemon=True)
        producer.start()

        try:
            while True:
                event = events.get(timeout=60)
                if event is None:
                    break
                if isinstance(event, Exception):
                    raise event
                yield normalize_azure_result(event)
        finally:
            recognizer.stop_continuous_recognition_async().get()
            stream.close()
            producer.join(timeout=1)

