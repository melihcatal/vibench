import os
from google.cloud import texttospeech

def generate_audio_preview(
    translated_text: str,
    language_code: str,
    output_filename: str = "audio_preview.mp3",
) -> str:
    """Generates an audio preview of translated copy using Google Cloud Text-to-Speech."""

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=translated_text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Can be MALE, FEMALE, or NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

    return f"Audio content written to file {output_filename}"
