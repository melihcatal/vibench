import azure.cognitiveservices.speech as speechsdk
from speech_models import SpeechConfig

def create_speech_recognizer(config: SpeechConfig, audio_stream: speechsdk.audio.PushAudioInputStream = None):
    speech_config = speechsdk.SpeechConfig(subscription=config.api_key, region=config.region)
    if config.language_code:
        speech_config.speech_recognition_language = config.language_code
    if config.enable_automatic_punctuation:
        speech_config.enable_punctuation = config.enable_automatic_punctuation

    if audio_stream:
        audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
    else:
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
