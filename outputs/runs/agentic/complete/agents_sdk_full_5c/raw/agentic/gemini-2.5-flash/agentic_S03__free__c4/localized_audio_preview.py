from google.cloud import texttospeech_v1

def generate_localized_audio_preview(text: str, language_code: str, ssml_gender: str = "NEUTRAL") -> bytes:
    """
    Generates spoken previews of translated copy using Google Cloud Text-to-Speech API.
    """
    client = texttospeech_v1.TextToSpeechClient()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    # Select the voice and audio file type
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech_v1.SsmlVoiceGender[ssml_gender],
    )

    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    return response.audio_content
