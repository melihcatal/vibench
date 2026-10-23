import os
from google.cloud import texttospeech_v1
from safety_client import GoogleSafetyClient


def generate_reviewer_brief_audio(brief_text: str) -> bytes:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get(
        "GOOGLE_CLOUD_LOCATION", "global"
    )  # Text-to-Speech is often global

    client = GoogleSafetyClient(project_id, location)

    synthesis_input = texttospeech_v1.SynthesisInput(text=brief_text)

    # Configure the voice
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )

    # Configure the audio format
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.text_to_speech_client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    audio_content = response.audio_content
    return audio_content
