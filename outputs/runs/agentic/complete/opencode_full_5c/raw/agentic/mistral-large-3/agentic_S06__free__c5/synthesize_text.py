from google.cloud import texttospeech_v1 as tts
from speech_client import TextToSpeechClient
from speech_models import (
    SynthesisRequest,
    VoiceSelection,
    AudioConfig,
    normalize_voice_selection,
    normalize_audio_config,
)


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: str = None,
    audio_encoding: str = "MP3",
) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = TextToSpeechClient().get_client()

    voice = VoiceSelection(language_code=language_code, name=voice_name)

    audio_config = AudioConfig(audio_encoding=audio_encoding)

    request = SynthesisRequest(text=text, voice=voice, audio_config=audio_config)

    response = client.synthesize_speech(
        input=tts.SynthesisInput(text=request.text),
        voice=tts.VoiceSelectionParams(**normalize_voice_selection(request.voice)),
        audio_config=tts.AudioConfig(**normalize_audio_config(request.audio_config)),
    )

    return response.audio_content
