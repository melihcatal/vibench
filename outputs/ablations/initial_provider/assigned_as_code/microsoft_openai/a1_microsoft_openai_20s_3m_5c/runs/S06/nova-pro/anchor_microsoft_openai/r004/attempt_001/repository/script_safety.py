import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config


def script_safety(payload, config=None):
    config = config or {}
    speech_config = get_speech_config(config)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = recognizer.recognize_once_async().get()
    if result.reason!= speechsdk.ResultReason.RecognizedSpeech:
        raise RuntimeError('Azure speech recognition failed')
    # Placeholder for actual safety check logic
    return {'is_safe': True}
