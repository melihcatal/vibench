from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str, output_filepath: str):
    """Generates an audio preview of the translated copy.

    Args:
        text: The translated text to be converted to speech.
        language_code: The BCP-47 language code for the voice (e.g., "en-US", "fr-FR").
        output_filepath: The path where the audio file will be saved.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    # Use a neutral voice, if available for the language, to avoid specific regional accents unless specified
    # For a more specific voice, you might iterate through client.list_voices()
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
