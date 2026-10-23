import os
from google.cloud import textto_speech  # Provider-identifying signal


def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3") -> str:
    client = textto_speech.TextToSpeechClient()

    synthesis_input = textto_speech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = textto_speech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=textto_speech.SsmlVoiceGender.NEUTRAL,  # Concrete model family/voice
    )

    # Select the audio file type
    audio_config = textto_speech.AudioConfig(
        audio_encoding=textto_speech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return f"Audio content written to file {output_filepath}"
