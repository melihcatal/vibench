import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_config():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    return speech_config

def create_push_audio_stream(sample_rate_hz):
    return speechsdk.audio.PushAudioInputStream(
        stream_format=speechsdk.audio.AudioStreamFormat(
            samples_per_second=sample_rate_hz, bits_per_sample=16, channels=1
        )
    )
