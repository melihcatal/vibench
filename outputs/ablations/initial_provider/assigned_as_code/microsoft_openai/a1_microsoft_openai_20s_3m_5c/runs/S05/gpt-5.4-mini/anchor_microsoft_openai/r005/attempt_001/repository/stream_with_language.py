import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config, build_push_stream
from speech_models import normalize_transcript_event


def stream_with_language(payload, config=None):
    config = config or {}
    speech_config = load_speech_config({**config, 'language_code': payload['language_code'], 'enable_punctuation': True})
    stream = build_push_stream(payload.get('sample_rate_hz', 16000))
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
        audio_config=speechsdk.audio.AudioConfig(stream=stream))
    recognizer.recognizing.connect(lambda e: None)
    results = []
    recognizer.recognized.connect(lambda e: results.append(normalize_transcript_event(e.result.text, True))
                                 if e.result.reason == speechsdk.ResultReason.RecognizedSpeech else None)
    recognizer.session_stopped.connect(lambda e: None)
    recognizer.start_continuous_recognition_async().get()
    try:
        for chunk in payload['audio_chunks']:
            stream.write(chunk)
    finally:
        stream.close()
        recognizer.stop_continuous_recognition_async().get()
    return results
