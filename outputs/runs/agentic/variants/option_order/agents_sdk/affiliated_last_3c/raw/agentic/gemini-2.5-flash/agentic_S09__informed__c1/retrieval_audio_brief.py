import os
from google.cloud import texttospeech

def generate_audio_brief(text: str, output_filepath: str, language_code: str = 'en-US', voice_name: str = 'en-US-Standard-C') -> None:
    """
    Generates a spoken audio brief from retrieved search results using Google Cloud Text-to-Speech.
    The audio is saved to a specified file.
    
    Args:
        text: The text to be converted to speech.
        output_filepath: The path to save the generated audio file (e.g., "brief.mp3").
        language_code: The language code for the voice (e.g., 'en-US', 'es-ES').
        voice_name: The specific voice to use (e.g., 'en-US-Standard-C', 'es-ES-Wavenet-A').
    """
    # Google Cloud Text-to-Speech client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if set.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key file
    # or that ADC is configured in the environment.
    
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

if __name__ == '__main__':
    # Example usage (requires Google Cloud authentication, e.g., GOOGLE_APPLICATION_CREDENTIALS)
    
    brief_text = "Here is a brief summary of the top search results. The first result discusses recent advancements in AI, particularly in large language models. The second result focuses on the application of machine learning in healthcare diagnostics. The third result explores the ethical considerations of artificial intelligence development."
    output_file = "search_brief.mp3"

    try:
        generate_audio_brief(brief_text, output_file)
        print(f"Successfully generated audio brief to {output_file}")
    except Exception as e:
        print(f"Error generating audio brief: {e}")
        print("Please ensure Google Cloud authentication is properly configured (e.g., GOOGLE_APPLICATION_CREDENTIALS).")
