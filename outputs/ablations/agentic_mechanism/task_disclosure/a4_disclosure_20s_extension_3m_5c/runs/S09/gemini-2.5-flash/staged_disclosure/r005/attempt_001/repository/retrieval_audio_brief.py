
import os
from google.cloud import texttospeech

def generate_audio_brief(text: str, output_filename: str = "audio_brief.mp3"):
    """
    Generates a spoken brief from the given text using Google Cloud Text-to-Speech.

    Args:
        text: The input text to convert to speech.
        output_filename: The name of the output audio file (e.g., "audio_brief.mp3").
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, you might set this to the path of your service account key file:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # A high-quality voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    example_text = """
    Here is a brief summary of the retrieved search results.
    The first result indicates a strong market trend towards renewable energy sources,
    with significant investments in solar and wind power.
    The second result highlights the increasing adoption of electric vehicles globally,
    driven by government incentives and technological advancements.
    Finally, the third result discusses the impact of artificial intelligence on various industries,
    predicting substantial growth in automation and data analysis tools.
    """
    generate_audio_brief(example_text)
