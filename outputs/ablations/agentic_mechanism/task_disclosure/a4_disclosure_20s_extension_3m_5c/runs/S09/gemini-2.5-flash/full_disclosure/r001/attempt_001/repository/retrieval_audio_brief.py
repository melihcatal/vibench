from google.cloud import texttospeech
import os

def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3"):
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.

    Args:
        text: The text content to be converted to speech.
        output_filepath: The path to save the generated audio file.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input with the plain text to be synthesized.
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("NEUTRAL")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

if __name__ == '__main__':
    # Example usage:
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS environment variable set
    # or authenticate otherwise for Google Cloud Text-to-Speech.
    # For local testing, you might need to set up your environment:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    sample_text = (
        "Here is a brief summary of the search results. "
        "The first result talks about the benefits of AI in healthcare. "
        "The second result discusses recent advancements in quantum computing. "
        "And the third result provides an overview of sustainable energy solutions."
    )
    generate_audio_brief(sample_text, "search_results_brief.mp3")
