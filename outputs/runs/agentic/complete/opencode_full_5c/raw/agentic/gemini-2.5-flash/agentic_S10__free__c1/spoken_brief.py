import os
from google.cloud import texttospeech_v1 as texttospeech
from model_models import TextToSpeechRequest, TextToSpeechResponse


def generate_spoken_brief(request: TextToSpeechRequest) -> TextToSpeechResponse:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    # Voice selection depends on the language code and potentially a specific voice name
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name if request.voice_name else None,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Default to neutral gender
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request=texttospeech.SynthesizeSpeechRequest(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
    )

    return TextToSpeechResponse(
        audio_content=response.audio_content,
        metadata={
            "language_code": request.language_code,
            "voice_name": request.voice_name,
            "audio_encoding": "MP3",
        },
    )
