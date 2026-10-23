import os
from google.cloud import speech_v1p1beta1 as speech
import azure.cognitiveservices.speech as azurespeech
import assemblyai as aai # AssemblyAI is a concrete third-party managed service

def get_google_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    return speech.SpeechClient()

def get_azure_speech_recognizer(language: str = "en-US"):
    """Initializes and returns an Azure SpeechRecognizer."""
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
    speech_config = azurespeech.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = language
    audio_config = azurespeech.AudioConfig(use_default_microphone=True) # For microphone input
    return azurespeech.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

def get_assemblyai_transcriber():
    """Configures and returns an AssemblyAI Transcriber."""
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY") # ASSEMBLYAI_API_KEY is a provider-identifying signal
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable must be set.")
    # The AssemblyAI transcriber is typically initialized directly with a session.
    # This function just ensures the API key is set for global usage or for session creation.
    pass
