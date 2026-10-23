import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filename: str = "spoken_brief.mp3"):
    """
    Generates a spoken brief from the given text using Google Cloud Text-to-Speech.

    Args:
        text (str): The text to convert to speech.
        output_filename (str): The name of the output MP3 file.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file '{output_filename}'")

if __name__ == "__main__":
    # Example usage:
    model_output = """
    The latest model analysis indicates a significant increase in user engagement
    following the recent feature update. Specifically, daily active users
    have grown by 15% over the past week, and session duration has increased
    by an average of 10 seconds. Customer feedback has been overwhelmingly positive,
    with many users highlighting the improved user interface and new functionalities.
    Further analysis will focus on long-term retention and conversion rates.
    """
    generate_spoken_brief(model_output)
