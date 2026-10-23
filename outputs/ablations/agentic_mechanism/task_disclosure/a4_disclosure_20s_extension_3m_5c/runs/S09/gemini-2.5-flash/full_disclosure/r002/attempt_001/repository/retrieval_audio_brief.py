import os
from google.cloud import texttospeech

def generate_audio_brief(search_results_text: str, output_filename: str = "audio_brief.mp3"):
    """Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.

    Args:
        search_results_text: The concatenated text of the search results.
        output_filename: The name of the output audio file (e.g., "audio_brief.mp3").
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=search_results_text)

    # Configure the voice. You can change the languageCode, ssmlGender, and name to fit your needs.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an output file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

if __name__ == '__main__':
    # Example usage:
    example_results = """
    Result 1: The quick brown fox jumps over the lazy dog.
    Result 2: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Result 3: This is a test of the emergency broadcast system.
    """
    generate_audio_brief(example_results, "my_audio_brief.mp3")
    print("Audio brief generated successfully: my_audio_brief.mp3")
