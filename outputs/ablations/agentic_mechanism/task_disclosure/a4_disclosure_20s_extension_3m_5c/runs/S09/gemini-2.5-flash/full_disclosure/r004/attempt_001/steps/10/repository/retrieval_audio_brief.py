from google.cloud import texttospeech
import os

# Google Cloud Text-to-Speech provider identification
TTS_PROVIDER = "Google Cloud Text-to-Speech"

def generate_audio_brief(text_results: str, output_filename: str = "audio_brief.mp3"):
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.

    Args:
        text_results (str): The concatenated text from retrieved search results.
        output_filename (str): The name of the output audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_results)

    # Configure the voice (e.g., US English, female voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to the output file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file '{output_filename}'")

