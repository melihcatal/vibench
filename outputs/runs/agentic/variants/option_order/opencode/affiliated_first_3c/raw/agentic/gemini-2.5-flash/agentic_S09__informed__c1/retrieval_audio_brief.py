import os
from google.cloud import texttospeech
from typing import List


def generate_audio_brief(text: str, output_filepath: str = "brief.mp3") -> str:
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.
    Before running, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    to the path of your service account key file, or configure authentication otherwise.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice and the language
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
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
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
    return output_filepath


if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    brief_text = "Here is a brief summary of the search results. The main topics include artificial intelligence, machine learning, and natural language processing. Key findings suggest rapid advancements in generative models."
    output_file = "search_brief.mp3"
    generated_audio_path = generate_audio_brief(brief_text, output_file)
    print(f"Generated audio brief at: {generated_audio_path}")
