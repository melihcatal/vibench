from typing import Optional
from speech_client import get_tts_client
from speech_models import VoiceParams, AudioConfig, create_speech_request
from google.cloud.texttospeech import SynthesizeSpeechResponse

def synthesize_ssml(ssml: str,
                    language_code: str = 'en-US',
                    voice_name: Optional[str] = None,
                    ssml_gender: Optional[str] = None,
                    **audio_kwargs) -> bytes:
    """
    Synthesizes SSML with voice and prosody controls to audio bytes using Google Cloud TTS.
    """
    client = get_tts_client()
    voice_params = VoiceParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=ssml_gender
    )
    audio_config = AudioConfig(**audio_kwargs)
    request = create_speech_request(ssml, is_ssml=True, voice_params=voice_params, audio_config=audio_config)
    response: SynthesizeSpeechResponse = client.synthesize_speech(request=request)
    return response.audio_content
