from google.cloud import texttospeech_v1 as tts
from speech_client import TextToSpeechClient
from speech_models import (
    SynthesisRequest,
    VoiceSelection,
    AudioConfig,
    normalize_voice_selection,
    normalize_audio_config,
)


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: str = None,
    audio_encoding: str = "MP3",
    speaking_rate: float = None,
    pitch: float = None,
    volume_gain_db: float = None,
) -> bytes:
    """
    Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.
    """
    client = TextToSpeechClient().get_client()

    voice = VoiceSelection(language_code=language_code, name=voice_name)

    audio_config = AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )

    request = SynthesisRequest(ssml=ssml, voice=voice, audio_config=audio_config)

    response = client.synthesize_speech(
        input=tts.SynthesisInput(ssml=request.ssml),
        voice=tts.VoiceSelectionParams(**normalize_voice_selection(request.voice)),
        audio_config=tts.AudioConfig(**normalize_audio_config(request.audio_config)),
    )

    return response.audio_content
