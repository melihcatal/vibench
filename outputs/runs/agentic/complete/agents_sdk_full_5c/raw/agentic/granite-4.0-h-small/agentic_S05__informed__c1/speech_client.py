import os
from ibm_watson import SpeechToTextV1
from google.cloud import speech_v1p1beta1 as speech
from azure.ai.speech import SpeechConfig, AudioDataStream, SpeechRecognizer
from deepgram.sdk import Client

# Consolidated speech client utilities
# Each provider offers a lightweight class exposing a .recognize_stream(iterable) method

# IBM Watson STT (WebSocket) client
# Credentials from env vars: IBM_STT_APIKEY, IBM_STT_URL
class WatsonSTTClient:
    def __init__(self):
        self.apikey = os.getenv('IBM_STT_APIKEY')
        self.url = os.getenv('IBM_STT_URL')
        self.speech_to_text = SpeechToTextV1(authenticator='iam')
        self.speech_to_text.set_service_url(self.url)
        self.speech_to_text.set_apikey(self.apikey)
    def recognize_stream(self, audio_iterable):
        # Use SDK's recognize_using_websocket which accepts an async iterator
        return self.speech_to_text.recognize_using_websocket(
            audio=next(audio_iterable),
            content_type='audio/l16; rate=16000',
            interim_results=True,
        )

# Google Cloud Speech-to-Text Streaming client
class GoogleSpeechClient:
    def __init__(self):
        self.client = speech.SpeechClient()
    def recognize_stream(self, audio_iterable):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            enable_automatic_punctuation=True,
        )
        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
        # Gather requests into list (the SDK expects an iterator)
        requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_iterable)
        return self.client.streaming_recognize(streaming_config, requests)

# Azure Speech SDK client
class AzureSpeechClient:
    def __init__(self):
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.region = os.getenv('AZURE_SPEECH_REGION')
        self.config = SpeechConfig(subscription=self.speech_key, region=self.region)
    def recognize_stream(self, audio_iterable):
        # Convert iterable to AudioDataStream (simplified)
        # Here we just pass the generator to the SDK's continuous recognition method
        audio_stream = AudioDataStream.from_iterable(audio_iterable)
        recognizer = SpeechRecognizer(self.config, audio_stream=audio_stream)
        # Recognize continuously returns final results; wrap to match API surface
        iterator = recognizer.recognize_once_async()
        return iterator

# Deepgram Streaming client
class DeepgramClient:
    def __init__(self):
        self.apikey = os.getenv('DEEPGRAM_API_KEY')
        self.client = Client(base_url='https://api.deepgram.io/v1')
        self.client.headers['Authorization'] = f'Bearer {self.apikey}'
    async def recognize_stream(self, audio_iterable):
        # Deepgram streaming API requires sending audio chunks via async HTTP
        # This stub shows the usage pattern; implement chunked upload per docs
        url = '/listen?model=english&tier=high'
        # Placeholder for actual async upload
        return None

# Create a registry (dictionary) for easy switching
SPEECH_CLIENTS = {
    'watson': WatsonSTTClient,
    'google': GoogleSpeechClient,
    'azure': AzureSpeechClient,
    'deepgram': DeepgramClient,
}

# Utility to instantiate a client by name and return its .recognize_stream() result
# Example usage:
# client = SPEECH_CLIENTS['google']().recognize_stream(audio_chunks())
# for response in client:
#     process(response)
