import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config


def stream_microphone():
    cfg = load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    speech_config.speech_recognition_language = cfg.language_code
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceConnection_EnableDictation,
        "true" if cfg.punctuate else "false",
    )
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    while True:
        result = recognizer.recognize_once_async().get()
        yield result.text
