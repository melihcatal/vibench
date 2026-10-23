from google.cloud import texttospeech

def synthesize_plain_text(text: str, language_code: str = "en-US", ssml_gender: str = "NEUTRAL") -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can be specified by language_code, name, and ssml_gender.
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=getattr(texttospeech.SsmlVoiceGender, ssml_gender.upper())
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
    # audio_bytes = synthesize_plain_text("Hello, this is a test from Google Cloud Text-to-Speech.", "en-US", "FEMALE")
    # with open("output_text.mp3", "wb") as out:
    #     out.write(audio_bytes)
    #     print('''Audio content written to "output_text.mp3"''')
    pass
