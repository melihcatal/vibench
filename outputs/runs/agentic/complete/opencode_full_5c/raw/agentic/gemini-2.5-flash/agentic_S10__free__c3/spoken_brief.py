import os
from google.cloud import texttospeech
from model_models import SpeechRequest, SpeechResponse


def generate_spoken_brief(request: SpeechRequest) -> SpeechResponse:
    """Generates a spoken brief from the model output using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()  # Using google.cloud.texttospeech_v1

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Default to neutral
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,  # MP3 is a common and widely supported format
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )

    response = client.synthesize_speech(
        request=texttospeech.SynthesizeSpeechRequest(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )
    )

    return SpeechResponse(audio_content=response.audio_content)
