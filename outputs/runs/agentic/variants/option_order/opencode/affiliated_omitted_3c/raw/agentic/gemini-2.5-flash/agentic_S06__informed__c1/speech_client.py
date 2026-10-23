import os
import azure.cognitiveservices.speech as speechsdk

def get_speech_synthesizer_client():
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Configure audio output to speaker for immediate playback or to a file for saving
    audio_config = speechsdk.audio.AudioOutputConfig(use_ Alber_speaker=False) # We will handle saving separately
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    return speech_synthesizer

def get_speech_recognizer_client(audio_file_path=None):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    if audio_file_path:
        audio_input = speechsdk.audio.AudioConfig(filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    else:
        # Default to microphone input if no file path is provided
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    return speech_recognizer
