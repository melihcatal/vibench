
from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str, output_filepath: str):
    """Generates a spoken audio preview of the given text using Google Cloud Text-to-Speech.

    Args:
        text: The text to be converted to speech.
        language_code: The BCP-47 language code for the voice (e.g., "en-US", "fr-FR").
        output_filepath: The path where the generated audio file will be saved.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the language and voice
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Or FEMALE, MALE
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
