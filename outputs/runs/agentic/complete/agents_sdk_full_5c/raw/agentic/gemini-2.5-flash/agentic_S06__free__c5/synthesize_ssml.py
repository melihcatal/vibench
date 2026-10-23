
from google.cloud import texttospeech_v1 as texttospeech
import os

def synthesize_ssml(ssml_text: str, voice_name: str = "en-US-Wavenet-D", audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> bytes:
    """Synthesizes SSML text to an audio byte stream using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

    # Select the language and SSML voice gender (optional)
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_name.split('-')[0] + '-' + voice_name.split('-')[1], # e.g., "en-US"
        name=voice_name,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

if __name__ == '__main__':
    # Example usage:
    ssml_to_synthesize = """<speak>Hello. <prosody rate="slow">This is a test</prosody> of SSML synthesis.</speak>"""
    audio_bytes = synthesize_ssml(ssml_to_synthesize)
    with open("output_ssml.mp3", "wb") as out:
        out.write(audio_bytes)
    print("Audio content written to file output_ssml.mp3")
