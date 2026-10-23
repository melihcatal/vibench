from google.cloud import texttospeech
from model_models import PlatformAudioBriefingRequest, PlatformAudioBriefingResponse


def generate_platform_brief_audio(
    request: PlatformAudioBriefingRequest,
) -> PlatformAudioBriefingResponse:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_encoding = texttospeech.AudioEncoding.MP3  # Defaulting to MP3 as per request
    if request.audio_encoding == "LINEAR16":
        audio_encoding = texttospeech.AudioEncoding.LINEAR16
    elif request.audio_encoding == "OGG_OPUS":
        audio_encoding = texttospeech.AudioEncoding.OGG_OPUS

    audio_config = texttospeech.AudioConfig(audio_encoding=audio_encoding)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return PlatformAudioBriefingResponse(
        audio_content=response.audio_content, provider="Google Cloud Text-to-Speech API"
    )
