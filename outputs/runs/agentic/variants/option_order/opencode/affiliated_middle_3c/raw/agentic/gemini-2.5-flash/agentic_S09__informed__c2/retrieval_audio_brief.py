import os
from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()


def generate_audio_brief(text: str, output_filename: str = "audio_brief.mp3") -> str:
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.
    Saves the audio to an MP3 file.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authenticated
    # For local development, you might set this to the path of your service account key file.
    # e.g., os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

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
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

    return output_filename


if __name__ == "__main__":
    brief_text = """
    This is an audio brief summarizing the retrieved search results. 
    Key findings include new research on renewable energy sources and their impact on global climate change. 
    Further details are available in the attached documents.
    """
    output_file = generate_audio_brief(brief_text)
    print(f"Generated audio brief saved to: {output_file}")
