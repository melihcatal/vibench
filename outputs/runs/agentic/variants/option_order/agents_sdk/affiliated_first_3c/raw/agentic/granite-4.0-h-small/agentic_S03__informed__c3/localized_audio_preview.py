import os
import io
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from gtts import gTTS

# Concrete provider chosen: IBM Watson Text to Speech (TTS)
# Provider is identified by the SDK import 'ibm_watson' and the service URL.

api_key = os.getenv('IBM_TTS_APIKEY')
service_url = os.getenv('IBM_TTS_URL', 'https://api.us-south.text-to-speech.watson.cloud.ibm.com')
authenticator = IAMAuthenticator(api_key)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(service_url)

def generate_audio_preview(text: str, target_lang: str = 'en-US', voice: str = 'en-US_MichaelV3Voice') -> bytes:
    """Generate a short audio preview of translated text using IBM Watson TTS.
    Returns the MP3 data as bytes.
    """
    # Use IBM TTS service directly for high quality
    response = tts.synthesize(text, accept='audio/mp3', voice=voice).get_result()
    audio_data = response.get('audio')
    if audio_data is None:
        raise RuntimeError('TTS service returned no audio')
    return audio_data

# Optional fallback using gTTS for quick preview (requires internet and may affect latency)

def generate_fallback_audio(text: str, target_lang: str = 'en') -> bytes:
    tts_obj = gTTS(text=text, lang=target_lang)
    audio_bytes = io.BytesIO()
    tts_obj.write_to_fp(audio_bytes)
    return audio_bytes.getvalue()

if __name__ == '__main__':
    demo = "Hello, welcome to the demo."
    audio = generate_audio_preview(demo, target_lang='es-ES', voice='es-ES_LauraV3Voice')
    with open('preview.mp3', 'wb') as f:
        f.write(audio)
    print('Audio preview written to preview.mp3')
