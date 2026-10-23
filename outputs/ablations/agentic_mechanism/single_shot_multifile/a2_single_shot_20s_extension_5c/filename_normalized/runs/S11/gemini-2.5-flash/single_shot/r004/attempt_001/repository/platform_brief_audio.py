import os
from google.cloud import texttospeech

# Ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key file
# or that gcloud auth application-default login has been run.

def generate_brief_audio(text: str, output_filepath: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A") -> str:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath