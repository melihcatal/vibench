from google.cloud import texttospeech
from model_models import ModelResponse

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"


def platform_brief_audio(response: ModelResponse) -> ModelResponse:
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech API.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=response.text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    tts_response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The audio content is binary.
    response.audio_content = tts_response.audio_content
    return response
