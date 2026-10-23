import azure.cognitiveservices.speech as speechsdk
import os

def get_speech_config() -> speechsdk.SpeechConfig:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")

    return speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

def get_microphone_audio_config() -> speechsdk.audio.AudioConfig:
    return speechsdk.audio.AudioConfig(use_microphone=True)

def get_push_audio_config() -> tuple[speechsdk.audio.PushAudioInputStream, speechsdk.audio.AudioConfig]:
    audio_input_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=audio_input_stream)
    return audio_input_stream, audio_config
