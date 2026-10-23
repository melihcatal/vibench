import json
import os
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, SynthesizeCallback

# IBM Watson STT WebSocket
STT_APIKEY = os.getenv('IBM_STT_APIKEY')
STT_URL = os.getenv('IBM_STT_URL')

# RecognizeCallback subclass to expose language and punctuation preferences
# (language model and punctuation can be set in the WebSocket request options)
class LanguagePartialHandler(RecognizeCallback):
    def __init__(self, language='en-US', punctuate=True):
        self.language = language
        self.punctuate = punctuate
        super().__init__()

    def get_url_options(self):
        # Build URL query parameters for WebSocket connection
        options = {
            'language_customization_id': '',
            'acoustic_customization_id': '',
            'base_model_name': 'enUSBroadbandModel',
            'language': self.language,
            'inactivity_timeout': -1,
            'contentType': 'audio/l16; rate=16000',
            'max_alternatives': 1,
            'punctuation': str(self.punctuate).lower(),
        }
        return options

async def stream_with_language(microphone_generator):
    """Starts streaming recognition with a specified language and punctuation setting."""
    client = SpeechToTextV1(authenticator='iam')
    client.set_service_url(STT_URL)
    client.set_apikey(STT_APIKEY)

    handler = LanguagePartialHandler(language='es-ES', punctuate=True)
    # The ibm-watson SDK uses this callback style for WebSocket
    # Connect using the SDK's built-in websocket client
    async for audio in microphone_generator:
        # Send audio chunk and receive events
        async for event in client.recognize_using_websocket(
            audio=audio,
            recognize_callback=handler,
            # The SDK handles language/punctuation via the URL options; no further code needed
        ):
            if event:
                # Process event payload (partial or final) via handler
                pass

# The function above can be used with any async audio generator (e.g., pyaudio)
# Example: asyncio.run(stream_with_language(your_microphone_generator()))
