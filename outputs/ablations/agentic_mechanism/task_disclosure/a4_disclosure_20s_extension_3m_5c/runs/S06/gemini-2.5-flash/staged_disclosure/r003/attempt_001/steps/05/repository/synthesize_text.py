from google.cloud import texttospeech
import os

def synthesize_text(text):
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech."""

    # Set up Google Cloud credentials (if not already set via environment variables)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

    client = texttospeech.TextToSpeechClient()

    input_text = textophen.SynthesisInput(text=text)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",  # Example voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The audio content is binary. You can save it to a file or stream it.
    return response.audio_content

if __name__ == "__main__":
    text_to_synthesize = "Hello, this is a test of the Google Cloud Text-to-Speech API."
    audio_bytes = synthesize_text(text_to_synthesize)

    with open("output.mp3", "wb") as out:
        out.write(audio_bytes)
        print('Audio content written to file "output.mp3"')
