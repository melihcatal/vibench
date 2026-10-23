import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_texttospeech_client() -> TextToSpeechV1:
    """Create and return a reusable IBM Watson Text to Speech client.
    Uses environment variables for configuration.
    Required env vars:
        IBM_TTS_APIKEY
        IBM_TTS_URL   (optional, defaults to public endpoint)
    """
    api_key = os.getenv('IBM_TTS_APIKEY')
    if not api_key:
        raise RuntimeError('Missing IBM_TTS_APIKEY environment variable')
    url = os.getenv('IBM_TTS_URL', 'https://api.us-south.text-to-speech.watson.cloud.ibm.com')
    authenticator = IAMAuthenticator(api_key)
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(url)
    return client
