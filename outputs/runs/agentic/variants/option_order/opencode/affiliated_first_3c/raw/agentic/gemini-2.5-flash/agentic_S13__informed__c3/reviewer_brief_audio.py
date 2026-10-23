import os
from google.cloud import texttospeech


def generate_reviewer_brief_audio(text: str, output_filepath: str) -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/your/credentials.json"
    )
    if "/path/to/your/credentials.json" in os.environ["GOOGLE_APPLICATION_CREDENTIALS"]:
        raise ValueError(
            "Google Cloud Text-to-Speech credentials must be set in environment variable GOOGLE_APPLICATION_CREDENTIALS"
        )

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # A high-quality Wavenet voice
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file '{output_filepath}'")

    return output_filepath
