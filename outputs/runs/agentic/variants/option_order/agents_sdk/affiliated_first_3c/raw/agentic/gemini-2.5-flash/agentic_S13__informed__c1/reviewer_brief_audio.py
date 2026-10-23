import os
from google.cloud import texttospeech

def reviewer_brief_audio(text: str, audio_file_path: str = "reviewer_brief.mp3"):
    # For Google Cloud Text-to-Speech, GOOGLE_APPLICATION_CREDENTIALS should be set up.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(audio_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {audio_file_path}")
    
    return {"audio_file_path": audio_file_path}
