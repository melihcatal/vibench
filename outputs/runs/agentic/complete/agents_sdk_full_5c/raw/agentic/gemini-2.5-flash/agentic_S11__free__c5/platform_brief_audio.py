from google.cloud import texttospeech

def generate_audio_briefing(text: str, output_filepath: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A"):
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
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

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
