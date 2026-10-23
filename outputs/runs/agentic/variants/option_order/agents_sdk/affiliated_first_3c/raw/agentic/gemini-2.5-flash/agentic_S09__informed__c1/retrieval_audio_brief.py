from google.cloud import texttospeech
import os

def generate_audio_brief(text: str, output_filepath: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-D") -> str:
    """Generates an audio brief from text using Google Cloud Text-to-Speech.

    Args:
        text: The text content for the audio brief.
        output_filepath: The path to save the generated audio file (e.g., 'brief.mp3').
        language_code: The BCP-47 language code for the voice (e.g., 'en-US').
        voice_name: The name of the voice to use (e.g., 'en-US-Wavenet-D').

    Returns:
        The path to the generated audio file if successful, otherwise an empty string.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # The client automatically picks up credentials from the environment.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # The response's audio_content is binary. Save it to a file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"Error generating audio brief with Google Cloud Text-to-Speech: {e}")
        return ""

