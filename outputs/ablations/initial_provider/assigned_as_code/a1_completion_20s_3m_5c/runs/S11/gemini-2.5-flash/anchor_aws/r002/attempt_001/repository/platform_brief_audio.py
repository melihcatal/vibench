import os
from google.cloud import texttospeech

def platform_brief_audio(text_output: str, project_id: str = None, voice_name: str = "en-US-Standard-C", audio_encoding: str = "MP3"):
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.
    """
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT_ID environment variable.")

    client = texttospeech.TextToSpeechClient() # Google Cloud Text-to-Speech client

    synthesis_input = texttospeech.SynthesisInput(text=text_output)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding)
    )

    # Select the voice parameters to use for the synthesis
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response audio_content is binary. We'll return it directly.
    # In a real application, you would typically save this to a file or stream it.
    return {"audio_content": response.audio_content, "audio_encoding": audio_encoding, "_provider_response": response}
