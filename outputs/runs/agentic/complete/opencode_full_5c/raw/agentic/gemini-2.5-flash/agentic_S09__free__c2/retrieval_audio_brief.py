from google.cloud import texttospeech
import os


def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3") -> str:
    # Google Cloud Text-to-Speech API client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the synthetic audio to the output file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return f"Audio content written to file {output_filepath}"
