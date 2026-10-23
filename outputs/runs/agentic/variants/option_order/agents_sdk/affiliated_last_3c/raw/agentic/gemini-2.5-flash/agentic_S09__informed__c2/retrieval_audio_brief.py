import os
from google.cloud import texttospeech

def generate_audio_brief(text_brief: str, output_filepath: str = "audio_brief.mp3") -> str:
    """
    Generates an audio brief from retrieved search results using Google Cloud Text-to-Speech.
    
    Args:
        text_brief: The text content of the brief.
        output_filepath: The path to save the generated audio file.
        
    Returns:
        The path to the saved audio file, or an error message if failed.
    """
    # Google Cloud Text-to-Speech uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure this environment variable is set or authentication is configured.
    
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file '{output_filepath}'")
        return output_filepath
    except Exception as e:
        print(f"Error generating audio brief with Google Cloud Text-to-Speech: {e}")
        return f"Failed to generate audio brief: {e}"

