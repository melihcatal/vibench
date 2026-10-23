import os
from google.cloud import texttospeech
from typing import Dict, Any

def generate_spoken_brief(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    text_to_speak = payload.get("text", "")
    output_audio_filename = payload.get("output_audio_filename", "spoken_brief.mp3")
    language_code = payload.get("language_code", "en-US")
    voice_name = payload.get("voice_name", "en-US-Standard-C") # Example voice name

    # Instantiates a client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS or default credentials are set up
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Example gender
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_audio_filename, "wb") as out:
        out.write(response.audio_content)

    return {"audio_filename": output_audio_filename, "message": f"Audio content written to {output_audio_filename}"}
