import os
from google.cloud import texttospeech

def localized_audio_preview(text: str, language_code: str, config: dict = None) -> bytes:
    config = config or {}
    project_id = config.get('project_id') or os.getenv('GOOGLE_CLOUD_PROJECT')

    if not project_id:
        # Text-to-Speech client does not strictly require project_id for basic synthesis
        pass

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML Voice Type
    # For specific voices, you might need to list available voices and choose one.
    # Using a neutral voice here. For example, 'en-US-Standard-C' or 'en-US-Wavenet-D'.
    # The voice name format often includes gender (e.g., 'en-US-Wavenet-A' is male, 'en-US-Wavenet-B' is female)
    # We'll pick a default based on language code or a generic one.
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary. You can save it to a file or stream it.
    return response.audio_content
