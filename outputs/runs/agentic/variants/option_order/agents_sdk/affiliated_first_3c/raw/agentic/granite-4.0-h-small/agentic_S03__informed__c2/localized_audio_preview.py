import os
import tempfile
import requests
from google.cloud import translate_v2 as translate
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Watson Text-to-Speech credentials
TTS_APIKEY = os.getenv('IBM_TTS_APIKEY')
TTS_URL = os.getenv('IBM_TTS_URL', 'https://api.us-south.text-to-speech.watson.cloud.ibm.com')
if not TTS_APIKEY:
    raise RuntimeError('Set IBM_TTS_APIKEY environment variable')

authenticator = IAMAuthenticator(TTS_APIKEY)
client = TextToSpeechV1(authenticator=authenticator)
client.set_service_url(TTS_URL)

TRANSLATE = translate.Client()

def localized_audio_preview(texts, target_lang='es'):
    """Translate texts and generate spoken audio preview files.
    Returns list of temporary .wav file paths.
    """
    temp_paths = []
    for txt in texts:
        translation = TRANSLATE.translate(txt, target_language=target_lang)['translatedText']
        audio = client.synthesize_using_voice(
            text=translation,
            accept='audio/wav',
            voice='en-US_MichaelV3Voice'
        ).get_result().content
        fd, path = tempfile.mkstemp(suffix='.wav')
        with open(path, 'wb') as f:
            f.write(audio)
        temp_paths.append(path)
    return temp_paths