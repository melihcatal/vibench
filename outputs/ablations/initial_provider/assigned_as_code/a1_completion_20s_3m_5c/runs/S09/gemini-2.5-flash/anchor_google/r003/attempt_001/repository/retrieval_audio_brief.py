import os
from typing import List, Dict, Any
from google.cloud import texttospeech

def retrieval_audio_brief(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, str]:
    config = config or {}
    brief_text = payload.get("brief_text")
    output_audio_filename = payload.get("output_audio_filename", "audio_brief.mp3")

    if not brief_text:
        raise ValueError("Payload must contain 'brief_text' string.")

    # Google Cloud Text-to-Speech API typically uses service account credentials
    # If not set explicitly, it will look for GOOGLE_APPLICATION_CREDENTIALS env var
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set up.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the language and SSML voice type
    # Using a common voice like en-US-Wavenet-D, you can choose others.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
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

    # The response's audio_content is binary. Write it to a file.
    with open(output_audio_filename, "wb") as out:
        out.write(response.audio_content)

    return {"audio_file": output_audio_filename, "message": f"Audio content written to file {output_audio_filename}"}
