import os
from google.cloud import texttospeech

def generate_audio_brief(text_results: str, output_filename: str = "audio_brief.mp3"):
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.

    Args:
        text_results (str): The concatenated text from search results to be spoken.
        output_filename (str): The name of the file to save the audio to.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_results)

    # Select the voice parameters. Google Cloud Text-to-Speech is the concrete provider.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example voice, choose an appropriate one
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

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file {output_filename}")

if __name__ == "__main__":
    # Example usage:
    search_results_text = "Here is a brief summary of your search results. The first result talks about artificial intelligence. The second result discusses machine learning applications. And the third result covers deep neural networks."
    generate_audio_brief(search_results_text)
