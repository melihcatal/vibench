from google.cloud import texttospeech
import os

def synthesize_ssml_text(ssml: str, voice_name: str = "en-US-Wavenet-C", audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> bytes:
    """Synthesizes SSML text to audio bytes using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

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
        ssml_to_synthesize = '''
<speak>
  Hello, this is a <prosody pitch="+10%" rate="slow">test</prosody> of SSML synthesis.
</speak>'''
        audio_data = synthesize_ssml_text(ssml_to_synthesize)
        print(f"Synthesized audio of length: {len(audio_data)} bytes")
        with open("output_ssml.mp3", "wb") as out:
            out.write(audio_data)
        print("Audio content written to file output_ssml.mp3")
