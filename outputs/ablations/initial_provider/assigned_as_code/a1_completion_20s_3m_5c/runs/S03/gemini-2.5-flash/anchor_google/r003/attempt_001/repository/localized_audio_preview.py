from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str, config: dict = None) -> bytes:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML Voice Gender (optional)
    # The voice name can be more specific, e.g., 'en-US-Standard-A'
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        request={'input': synthesis_input, 'voice': voice, 'audio_config': audio_config}
    )

    # The response's audio_content is binary. You might save it to a file or stream it.
    return response.audio_content
