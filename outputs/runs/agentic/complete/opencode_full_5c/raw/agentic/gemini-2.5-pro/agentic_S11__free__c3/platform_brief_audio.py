from model_client import get_google_tts_client
from model_models import AudioResponse
from google.cloud import texttospeech


def generate_audio_briefing(text: str) -> AudioResponse:
    tts_client = get_google_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioResponse(audio_content=response.audio_content)
