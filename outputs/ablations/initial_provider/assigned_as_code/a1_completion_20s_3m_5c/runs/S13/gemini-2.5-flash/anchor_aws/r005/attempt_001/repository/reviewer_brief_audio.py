import os
from typing import Dict, Any
from google.cloud import texttospeech

def generate_reviewer_brief_audio(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    # Google Cloud credentials are typically handled by GOOGLE_APPLICATION_CREDENTIALS
    # or by running in a Google Cloud environment.
    # Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # the application is running in a GCP environment with appropriate permissions.

    client = texttospeech.TextToSpeechClient()

    brief_text = payload["brief_text"]
    output_audio_encoding = payload.get("output_audio_encoding", texttospeech.AudioEncoding.MP3) # Default to MP3
    language_code = payload.get("language_code", "en-US")
    voice_name = payload.get("voice_name", "en-US-Standard-C") # Example voice

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the type of audio file you want to generate
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=output_audio_encoding
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The audio content is in base64 encoded bytes. Convert to string for return.
    audio_content_base64 = response.audio_content.hex() # Convert bytes to hex string for easier handling/storage

    return {
        "brief_text": brief_text,
        "audio_content": audio_content_base64,
        "audio_encoding": output_audio_encoding.name # Return the name of the encoding
    }
