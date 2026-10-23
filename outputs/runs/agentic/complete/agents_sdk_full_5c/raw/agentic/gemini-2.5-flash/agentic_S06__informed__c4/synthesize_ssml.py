import os
from google.cloud import texttospeech

def synthesize_ssml_text(ssml_text: str, output_filepath: str = "output_ssml.mp3", voice_name: str = "en-US-Standard-W", language_code: str = "en-US"):
    """Synthesizes SSML text to an audio file using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # Example SSML:
    # ssml = "<speak>Hello. <prosody rate=\"slow\">This is a test</prosody> of SSML synthesis.</speak>"
    # synthesize_ssml_text(ssml, "ssml_example.mp3")
    pass
