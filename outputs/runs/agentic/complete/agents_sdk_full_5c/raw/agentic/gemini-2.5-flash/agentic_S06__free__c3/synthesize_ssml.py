from google.cloud import texttospeech

def synthesize_ssml_with_controls(ssml: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-A") -> bytes:
    """Synthesizes SSML with specified voice and prosody controls using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Select the type of audio file you want to generate
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # ssml_text = '''<speak>Hello, <prosody rate="slow">this is a very slow voice.</prosody> I can also speak in a <emphasis level="strong">strong</emphasis> tone.</speak>'''
    # audio_bytes = synthesize_ssml_with_controls(ssml_text, "en-US", "en-US-Wavenet-F")
    # with open("output_ssml.mp3", "wb") as out:
    #     out.write(audio_bytes)
    #     print('''Audio content written to "output_ssml.mp3"''')
    pass
