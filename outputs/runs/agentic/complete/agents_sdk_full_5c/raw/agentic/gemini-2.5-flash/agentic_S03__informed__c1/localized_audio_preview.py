from google.cloud import texttospeech
import os

def generate_audio_preview(text: str, language_code: str, voice_name: str = None, audio_file_path: str = "output.mp3") -> str:
    """Generates a spoken preview of translated copy using Google Cloud Text-to-Speech.

    Args:
        text: The text to convert to speech.
        language_code: The BCP-47 language code, e.g., 'en-US', 'es-ES', 'fr-FR'.
        voice_name: The name of the voice to use, e.g., 'en-US-Wavenet-D'. If None, a default voice is chosen.
        audio_file_path: The path to save the generated audio file.

    Returns:
        The path to the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    if voice_name:
        voice_selection_params = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
    else:
        voice_selection_params = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Default to a neutral gender if no specific voice is provided
        )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Save it to a file.
    with open(audio_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{audio_file_path}'')
    
    return audio_file_path
