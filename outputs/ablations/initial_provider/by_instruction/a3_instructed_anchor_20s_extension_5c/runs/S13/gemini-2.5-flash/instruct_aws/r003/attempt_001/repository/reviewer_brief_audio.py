from google.cloud import texttospeech

def generate_reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3") -> str:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Using a specific voice parameter
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3 # Using a specific audio encoding
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
    
    return output_filepath
