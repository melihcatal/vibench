import os
from google.cloud import texttospeech

def generate_audio_brief(text_content, output_filename="audio_brief.mp3"):
    """
    Generates a spoken brief from text content using Google Cloud Text-to-Speech.

    Args:
        text_content (str): The text to be converted to speech.
        output_filename (str): The name of the output audio file (e.g., "audio_brief.mp3").

    Returns:
        str: The path to the generated audio file, or None if an error occurred.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = textotexttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    try:
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        return output_filename
    except Exception as e:
        print(f"Error writing audio file: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    search_results_text = """
    Here is a brief summary of the retrieved search results.
    The first result talks about the benefits of artificial intelligence in healthcare.
    The second result discusses recent advancements in quantum computing.
    The third result highlights the impact of climate change on global weather patterns.
    """
    audio_file = generate_audio_brief(search_results_text)
    if audio_file:
        print(f"Audio brief generated and saved to {audio_file}")
    else:
        print("Failed to generate audio brief.")
