import os
from google.cloud import texttospeech_v1
from translation_client import get_text_to_speech_client

def generate_localized_audio_preview(
    text: str,
    language_code: str,
    voice_name: str = "en-US-Standard-A", # Example voice, adjust as needed
    output_file_path: str = "audio_preview.mp3",
) -> str:
    """Generates spoken previews of translated copy using Google Cloud Text-to-Speech."""
    client = get_text_to_speech_client()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    # Select the language and SSML voice gender (optional)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
    return f"Audio content written to file {output_file_path}"

