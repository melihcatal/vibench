from google.cloud import texttospeech_v1 as texttospeech

def platform_brief_audio(text: str, output_filepath: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A"):
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Can be MALE, FEMALE, NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config
        }
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

    return {
        "text_input": text,
        "output_filepath": output_filepath,
        "audio_length_bytes": len(response.audio_content)
    }
