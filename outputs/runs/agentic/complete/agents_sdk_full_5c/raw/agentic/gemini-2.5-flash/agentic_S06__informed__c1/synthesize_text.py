from google.cloud import texttospeech
import os

def synthesize_plain_text(text: str, voice_name: str = "en-US-Wavenet-C", audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> bytes:
    """Synthesizes plain text to audio bytes using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    else:
        text_to_synthesize = "Hello, this is a test of Google Cloud Text-to-Speech."
        audio_data = synthesize_plain_text(text_to_synthesize)
        print(f"Synthesized audio of length: {len(audio_data)} bytes")
        with open("output_text.mp3", "wb") as out:
            out.write(audio_data)
        print("Audio content written to file output_text.mp3")
