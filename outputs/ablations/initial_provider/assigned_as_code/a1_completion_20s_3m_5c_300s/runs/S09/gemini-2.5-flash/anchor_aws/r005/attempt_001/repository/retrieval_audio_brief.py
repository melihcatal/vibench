import os
from google.cloud import texttospeech

def retrieval_audio_brief(text, output_filepath, config=None):
    config = config or {}
    # Google Cloud Text-to-Speech API typically uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure the environment variable is set or pass credentials explicitly if needed.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set up.
    
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio format.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request.
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the audio content to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        
    return {"audio_filepath": output_filepath, "status": "success"}
