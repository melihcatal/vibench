
import os
from google.cloud import texttospeech

def generate_audio_brief(text_to_speak: str, output_filename: str = "audio_brief.mp3"):
    """
    Generates a spoken brief from the given text using Google Cloud Text-to-Speech.

    Args:
        text_to_speak: The text content to be converted to speech.
        output_filename: The name of the output audio file (e.g., "audio_brief.mp3").
    """

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
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
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Replace this with your actual retrieved search results
    search_results_text = """
    According to recent studies, climate change is accelerating, leading to more frequent extreme weather events.
    Efforts to reduce carbon emissions are ongoing globally, with renewable energy sources playing a crucial role.
    New research suggests that advancements in carbon capture technology could also contribute significantly to mitigation.
    """
    generate_audio_brief(search_results_text)
