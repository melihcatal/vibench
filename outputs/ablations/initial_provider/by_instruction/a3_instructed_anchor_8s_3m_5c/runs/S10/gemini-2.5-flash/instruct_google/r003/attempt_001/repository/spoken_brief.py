import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filepath: str, voice_name: str = "en-US-Wavenet-D") -> None:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,  # e.g., "en-US-Wavenet-D" for a specific voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
