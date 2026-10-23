from translation_client import get_google_tts_client
from google.cloud import texttospeech


def generate_audio_preview(text: str, language_code: str, output_file: str):
    """
    Generates a spoken audio preview of translated text.

    Args:
        text: The text to synthesize.
        language_code: The BCP-47 language code (e.g., 'en-US', 'es-ES').
        output_file: The path to save the output audio file (e.g., 'preview.mp3').
    """
    client = get_google_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')
