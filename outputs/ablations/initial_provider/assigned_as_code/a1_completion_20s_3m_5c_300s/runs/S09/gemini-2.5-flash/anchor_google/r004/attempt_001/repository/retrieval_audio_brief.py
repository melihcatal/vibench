import os
from typing import List, Dict
from google.cloud import texttospeech
from embeddings_models import GOOGLE_TTS_VOICE_NAME

def retrieval_audio_brief(payload: Dict, config: Dict = None) -> Dict:
    config = config or {}
    # Google Cloud Text-to-Speech API typically uses application default credentials
    # or GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # No explicit API key is usually passed here for server-side auth.

    client = texttospeech.TextToSpeechClient()

    brief_text = payload.get("brief_text")
    output_filename = payload.get("output_filename", "audio_brief.mp3")

    if not isinstance(brief_text, str) or not brief_text:
        raise ValueError("Payload must contain a 'brief_text' key with a string.")
    if not isinstance(output_filename, str) or not output_filename:
        raise ValueError("Payload must contain an 'output_filename' key with a string (e.g., 'brief.mp3').")

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=GOOGLE_TTS_VOICE_NAME, # Using a standard US English voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # The response's audio_content is binary. Write it to a file.
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)

        return {"status": "success", "output_file": output_filename, "message": f"Audio content written to {output_filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
