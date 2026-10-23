from google.cloud import texttospeech
from speech_client import get_tts_client

def synthesize_and_save(text: str, output_path: str):
    """
    Synthesizes text to speech and saves the audio to a file using Google Cloud TTS.

    Args:
        text: The text to synthesize.
        output_path: The path to save the resulting MP3 file.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_path, "wb") as out:
        out.write(response.audio_content)
