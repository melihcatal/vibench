import os
from google.cloud import texttospeech_v1 as texttospeech

def generate_audio_preview(text: str, language_code: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and voice.
    # The voice_name should be compatible with the language_code.
    # For example, 'en-US-Wavenet-D' is for English (United States).
    # The SsmlVoiceGender can be adjusted as needed.
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Can be FEMALE, MALE, NEUTRAL
    )

    # Select the type of audio file you want returned.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    response = client.synthesize_speech(request=request)

    # The response's audio_content is binary. You might save it to a file or stream it.
    return response.audio_content
