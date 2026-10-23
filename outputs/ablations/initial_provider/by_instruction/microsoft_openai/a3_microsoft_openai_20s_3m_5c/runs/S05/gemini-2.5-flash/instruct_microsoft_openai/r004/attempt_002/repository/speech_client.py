import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config():
    speech_key = os.environ.get("SPEECH_KEY")
    service_region = os.environ.get("SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("Please set the SPEECH_KEY and SPEECH_REGION environment variables.")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Configure for interim results
    speech_config.request_word_level_timestamps()
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    return speech_config

def get_audio_config_from_microphone():
    return speechsdk.AudioConfig(use_ microphone=True)

def get_audio_config_from_stream():
    # Placeholder for audio stream input
    return speechsdk.audio.AudioConfig(stream=speechsdk.audio.PushAudioInputStream())
