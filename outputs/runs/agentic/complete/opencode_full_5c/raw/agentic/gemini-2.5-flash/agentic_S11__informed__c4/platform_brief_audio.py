from google.cloud import texttospeech
import os
from model_models import AudioBriefing


def platform_brief_audio(
    text: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A"
) -> AudioBriefing:
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.

    Args:
        text: The text to convert to speech.
        language_code: The language code for the voice (e.g., "en-US").
        voice_name: The desired voice name (e.g., "en-US-Standard-A").

    Returns:
        An AudioBriefing object containing the audio content and format.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Can be MALE, FEMALE, or NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The audio content is binary data
    audio_content = response.audio_content
    audio_format = "mp3"

    return AudioBriefing(audio_content=audio_content, audio_format=audio_format)
