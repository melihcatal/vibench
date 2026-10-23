import os
from google.cloud import texttospeech
from model_models import LLMResponse
import base64


def generate_spoken_brief(
    text: str, language_code: str = "en-US", voice_name: str = "en-US-Neural2-C"
) -> LLMResponse:
    """
    Generates a spoken brief (audio) from the model output using Google Cloud Text-to-Speech.
    Returns the audio content as a base64 encoded string.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and voice
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,  # Example: "en-US-Standard-C", "en-US-Wavenet-C", "en-US-Neural2-C"
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The audio content is binary, encode it to base64 for easy transport/storage
    audio_content_base64 = base64.b64encode(response.audio_content).decode("utf-8")

    return LLMResponse(
        text="Spoken brief generated successfully.",
        metadata={
            "audio_provider": "google_cloud_text_to_speech",
            "language_code": language_code,
            "voice_name": voice_name,
            "audio_encoding": "MP3",
            "audio_content_base64": audio_content_base64,
        },
    )
