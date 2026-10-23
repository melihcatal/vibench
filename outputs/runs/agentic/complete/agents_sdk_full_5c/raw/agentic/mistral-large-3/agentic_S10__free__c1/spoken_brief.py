import os
from typing import Optional
from google.cloud import texttospeech_v1 as texttospeech

_GOOGLE_TTS_CREDENTIALS = os.getenv("GOOGLE_TTS_CREDENTIALS_JSON")


def generate_spoken_brief(
    text: str,
    output_file: str = "output.mp3",
    voice_name: str = "en-US-Wavenet-D",
    language_code: str = "en-US"
) -> str:
    """
    Generate a spoken brief from the model output using Google Cloud Text-to-Speech API.
    """
    if _GOOGLE_TTS_CREDENTIALS:
        client = texttospeech.TextToSpeechClient.from_service_account_json(_GOOGLE_TTS_CREDENTIALS)
    else:
        client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    return output_file