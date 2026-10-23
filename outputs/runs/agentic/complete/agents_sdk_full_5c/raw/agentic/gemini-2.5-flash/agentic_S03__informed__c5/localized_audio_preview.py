import os
from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str, voice_name: str = None, audio_file_path: str = "output.mp3") -> str:
    """Generates a spoken preview of translated copy using Google Cloud Text-to-Speech.

    Args:
        text: The text to convert to speech.
        language_code: The BCP-47 language code for the voice (e.g., "en-US", "es-ES").
        voice_name: (Optional) The name of the voice to use (e.g., "en-US-Standard-C").
                    If not provided, a default will be chosen based on language_code.
        audio_file_path: The path to save the generated audio file.

    Returns:
        The path to the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    if voice_name:
        voice_selection = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
    else:
        voice_selection = texttospeech.VoiceSelectionParams(
            language_code=language_code
        )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(audio_file_path, "wb") as out:
        out.write(response.audio_content)

    return audio_file_path

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS env var)
    # translated_copy = "Hola, ¿cómo estás?"
    # lang_code = "es-ES"
    # output_file = "hola_es.mp3"
    # audio_path = generate_audio_preview(translated_copy, lang_code, audio_file_path=output_file)
    # print(f"Audio content written to {audio_path}")

    # translated_copy_en = "Hello, how are you?"
    # lang_code_en = "en-US"
    # output_file_en = "hello_en.mp3"
    # audio_path_en = generate_audio_preview(translated_copy_en, lang_code_en, voice_name="en-US-Neural2-C", audio_file_path=output_file_en)
    # print(f"Audio content written to {audio_path_en}")
    pass
