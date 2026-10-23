from google.cloud import texttospeech

def synthesize_ssml(ssml_text: str, voice_name: str, language_code: str, audio_encoding: texttospeech.AudioEncoding) -> bytes:
    """
    Synthesizes SSML text to audio using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config
    )

    return response.audio_content
