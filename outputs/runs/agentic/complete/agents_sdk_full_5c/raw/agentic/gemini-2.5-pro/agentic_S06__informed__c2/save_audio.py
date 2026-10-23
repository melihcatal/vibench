from synthesize_text import synthesize_text_to_audio

def save_audio_to_file(
    text: str, voice_name: str, language_code: str, output_path: str
) -> None:
    """
    Synthesizes text using Google Cloud TTS and saves the audio to a file.

    This function demonstrates the end-to-end process from text to a saved audio file,
    making it dependent on the Google Cloud Text-to-Speech provider integration.

    Args:
        text: The text to synthesize.
        voice_name: The voice name for synthesis.
        language_code: The language code for synthesis.
        output_path: The path to save the resulting MP3 file.
    """
    audio_content = synthesize_text_to_audio(text, voice_name, language_code)
    
    with open(output_path, "wb") as out:
        out.write(audio_content)
