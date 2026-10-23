import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config, make_azure_speech_config


def stream_with_language(language: str = "en-US", punctuation: bool = True):
    cfg = load_speech_config()
    cfg.language = language
    cfg.enable_punctuation = punctuation
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    speech_config.speech_recognition_language = cfg.language
    if punctuation:
        speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText"
        )
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    return recognizer
