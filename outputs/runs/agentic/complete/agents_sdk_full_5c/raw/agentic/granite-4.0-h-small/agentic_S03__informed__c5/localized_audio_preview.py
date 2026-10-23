import os
import pydub
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def preview_audio(translated_text: str, voice: str = 'en-US_MichaelV3Voice') -> bytes:
    """Generate spoken preview of translated copy using IBM Watson Text to Speech.",
    api_key = os.getenv('IBM_TTS_APIKEY')
    service_url = os.getenv('IBM_TTS_URL')
    if not api_key or not service_url:
        raise RuntimeError('IBM TTS credentials not set')
    authenticator = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(service_url)
    audio = tts.synthesize(text=translated_text, accept='audio/wav', voice=voice).get_result()
    return audio.get_result()  # binary wav data
