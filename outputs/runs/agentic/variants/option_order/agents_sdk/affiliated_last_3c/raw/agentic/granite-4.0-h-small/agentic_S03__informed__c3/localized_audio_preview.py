import os
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech

# Local helpers
from translation_client import get_translation_client
from translation_models import validate_language_code, validate_text

# Choose a voice for TTS; adjust language code as needed
VOICE_NAME = "en-US-Wavenet-D"

def generate_audio_preview(translated_text: str, target_lang: str, output_path: str = "preview.mp3") -> None:
    """Generates a spoken audio preview of translated text using Cloud Text-to-Speech.

    Args:
        translated_text: Text to be spoken.
        target_lang: Language code for the voice (e.g., 'es', 'fr').
        output_path: File path to write the generated MP3.
    """
    client = get_translation_client()
    validate_language_code(target_lang)
    validated = validate_text(translated_text)
    # Text-to-Speech client
    tts_client = texttospeech.TextToSpeechClient()
    input_ssml = texttospeech.SynthesisInput(ssml=f"<speak>{validated}</speak>")
    voice = texttospeech.VoiceSelectionParams(
        language_code=target_lang,
        name=VOICE_NAME
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = tts_client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    with open(output_path, 'wb') as out_f:
        out_f.write(response.audio_content)
    print(f"Audio preview saved to {output_path}")

if __name__ == "__main__":
    sample = "Hello, welcome to the preview."
    generate_audio_preview(sample, "es")