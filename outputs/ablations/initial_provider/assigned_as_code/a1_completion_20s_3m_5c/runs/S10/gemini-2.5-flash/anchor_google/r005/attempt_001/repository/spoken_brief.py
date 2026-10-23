import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, config: dict = None) -> dict:
    config = config or {}
    # Google Cloud Text-to-Speech API client does not require explicit project_id if GOOGLE_APPLICATION_CREDENTIALS is set
    # or running in a Google Cloud environment.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The audio content is in `response.audio_content`
    # You might want to save it to a file or return it directly.
    # For this example, we return it as bytes (base64 encoded if passing over JSON usually, but here raw bytes).
    return {"audio_content": response.audio_content}
