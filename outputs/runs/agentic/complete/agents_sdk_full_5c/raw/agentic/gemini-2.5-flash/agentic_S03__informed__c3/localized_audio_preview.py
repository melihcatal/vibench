import os
from google.cloud import texttospeech_v1 as texttospeech

def generate_audio_preview(
    text: str,
    language_code: str,
    voice_name: str = "en-US-Standard-A", # Example voice, adjust as needed
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3,
    output_filepath: str = "audio_preview.mp3",
) -> str:
    """
    Generates a spoken preview of translated copy using Google Cloud Text-to-Speech.
    Returns the path to the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code and the SSML voice gender
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

    return output_filepath
