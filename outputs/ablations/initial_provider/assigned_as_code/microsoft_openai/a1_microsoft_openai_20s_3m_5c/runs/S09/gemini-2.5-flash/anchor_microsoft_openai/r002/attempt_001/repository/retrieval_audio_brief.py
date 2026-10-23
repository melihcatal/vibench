import os
from google.cloud import texttospeech
from typing import List, Dict, Any

def retrieval_audio_brief(text_brief: str, output_filepath: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    # Google Cloud project ID and credentials assumed to be set up via environment variables.

    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Build the voice request, select the language code (e.g., "en-US") and the ssml
    # voice gender (e.g., male, female).
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # or MALE, FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )

        # The response's audio_content is binary. Write it to a file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        
        return {'status': 'success', 'output_filepath': output_filepath}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}
