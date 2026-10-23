import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def platform_brief_audio(output_text: str, voice: str = 'en-US_AllisonV3Voice') -> bytes:
    """Generate spoken briefing from model output using IBM Watson Text to Speech."""
    apikey = os.getenv('IBM_TTS_APIKEY')
    service_url = os.getenv('IBM_TTS_URL')
    if not apikey or not service_url:
        raise RuntimeError('IBM TTS credentials not configured')
    authenticator = IAMAuthenticator(apikey)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(service_url)
    response = tts.synthesize(output_text, accept='audio/mp3', voice=voice).get_result()
    return response.content
