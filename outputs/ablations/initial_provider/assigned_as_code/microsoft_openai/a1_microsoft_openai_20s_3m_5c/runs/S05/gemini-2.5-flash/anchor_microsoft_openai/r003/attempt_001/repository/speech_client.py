import azure.cognitiveservices.speech as speechsdk

def get_speech_config(api_key: str, region: str, language_code: str = "en-US", enable_punctuation: bool = False):
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language = language_code
    if enable_punctuation:
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText")
    return speech_config

def get_audio_config_from_stream(stream):
    return speechsdk.audio.AudioConfig(stream=stream)

def get_push_audio_input_stream(sample_rate_hz: int, bits_per_sample: int = 16, channels: int = 1):
    return speechsdk.audio.PushAudioInputStream(speechsdk.audio.AudioStreamFormat(
        samples_per_second=sample_rate_hz, bits_per_sample=bits_per_sample, channels=channels))

def get_speech_recognizer(speech_config, audio_config):
    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
