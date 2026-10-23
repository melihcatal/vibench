from google.cloud import texttospeech

def platform_brief_audio(text_content: str, output_file_path: str):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Select the language and voice
    # Using a standard US English voice. You can choose other voices and languages.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        
    return {"audio_file_path": output_file_path, "audio_content_length": len(response.audio_content)}
