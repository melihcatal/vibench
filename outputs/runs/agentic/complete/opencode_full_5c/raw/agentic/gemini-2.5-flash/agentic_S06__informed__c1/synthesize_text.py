import os
from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from speech_models import VoiceSelection, SynthesisInput, AudioConfig


def synthesize_plain_text(
    text: str,
    output_filename: str,
    voice_selection: VoiceSelection,
    audio_config: AudioConfig,
):
    """
    Synthesizes plain text to an audio byte stream and saves it to a file.
    """
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_selection.language_code,
        name=voice_selection.name,
        ssml_gender=texttospeech.SsmlVoiceGender[voice_selection.ssml_gender]
        if voice_selection.ssml_gender
        else None,
    )

    audio_configuration = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[audio_config.audio_encoding],
        speaking_rate=audio_config.speaking_rate,
        pitch=audio_config.pitch,
        volume_gain_db=audio_config.volume_gain_db,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_configuration
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
