from google.cloud import texttospeech

def platform_brief_audio(text_content: str, project_id: str, output_audio_file: str = "output.mp3"):
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the voice parameters. For example, a female voice with a Wavenet model.
    # You can explore other voices in the documentation.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        name="en-US-Wavenet-F" # A specific Wavenet voice
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an output file.
    with open(output_audio_file, "wb") as out:
        out.write(response.audio_content)

    return {"audio_file_path": output_audio_file}
