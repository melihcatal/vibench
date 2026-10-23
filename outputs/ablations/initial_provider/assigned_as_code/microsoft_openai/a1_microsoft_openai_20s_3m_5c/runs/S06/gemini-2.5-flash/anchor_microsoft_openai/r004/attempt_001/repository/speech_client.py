import azure.cognitiveservices.speech as speechsdk
from speech_models import TextToSpeechConfig

def get_speech_config(config: TextToSpeechConfig) -> speechsdk.SpeechConfig:
    speech_config = speechsdk.SpeechConfig(subscription=config.api_key, region=config.region)
    if config.voice:
        speech_config.speech_synthesis_voice_name = config.voice
    if config.output_format:
        speech_config.set_speech_synthesis_output_format(getattr(speechsdk.SpeechSynthesisOutputFormat, config.output_format))
    return speech_config
