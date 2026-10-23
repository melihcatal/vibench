from google.cloud import texttospeech

def platform_brief_audio(text_output: str, audio_file_path: str):
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_output)

    # Select the type of audio file you want to generate
    # Choose a voice that suits your needs
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(audio_file_path, "wb") as out:
        out.write(response.audio_content)
        
    return {"audio_file_path": audio_file_path, "audio_size_bytes": len(response.audio_content)}
