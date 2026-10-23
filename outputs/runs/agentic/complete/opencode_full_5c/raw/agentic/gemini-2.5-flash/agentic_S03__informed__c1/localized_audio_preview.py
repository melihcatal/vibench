from translation_client import get_text_to_speech_client
from google.cloud import texttospeech


def generate_audio_preview(
    text: str, language_code: str, voice_name: str = "en-US-Standard-A"
) -> bytes:
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the voice parameters.
    # For a list of available voices, see https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. You can save it or play it.
    return response.audio_content
