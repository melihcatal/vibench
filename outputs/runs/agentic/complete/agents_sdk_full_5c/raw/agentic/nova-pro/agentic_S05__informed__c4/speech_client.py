import azure.cognitiveservices.speech as speechsdk

def create_speech_config(subscription_key, region, language="en-US"):
    return speechsdk.SpeechConfig(subscription=subscription_key, region=region, speech_recognition_language=language)

def create_audio_config(use_default_microphone=True, filename=None):
    if use_default_microphone:
        return speechsdk.audio.AudioConfig(use_default_microphone=True)
    else:
        return speechsdk.audio.AudioConfig(filename=filename)

def create_speech_recognizer(speech_config, audio_config):
    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)