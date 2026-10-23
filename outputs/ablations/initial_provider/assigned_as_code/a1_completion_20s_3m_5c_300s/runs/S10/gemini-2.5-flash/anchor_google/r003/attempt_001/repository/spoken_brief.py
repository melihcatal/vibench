import os
from typing import Any, Dict
from google.cloud import texttospeech

def spoken_brief(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    
    text_to_speak = payload.get("text", "")
    if not text_to_speak:
        raise ValueError("Payload must contain 'text' for spoken brief generation.")

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)

    # Build the voice request, select the language code (e.g., "en-US") and the ssml
    # voice gender (e.g., ssml_voice_gender.FEMALE)
    voice = texttospeech.VoiceSelectionParams(
        language_code=config.get("language_code", "en-US"),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. We return it as bytes.
    return {"audio_content": response.audio_content}
