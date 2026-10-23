import os
from typing import Dict, Any
from google.cloud import texttospeech

def reviewer_brief_audio(text: str, output_filepath: str, config: Dict[str, Any] = None) -> str:
    config = config or {}
    
    # Initialize Google Cloud Text-to-Speech client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authenticated otherwise
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=config.get("language_code", "en-US"),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Can be MALE, FEMALE, NEUTRAL
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
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
    
    return output_filepath
