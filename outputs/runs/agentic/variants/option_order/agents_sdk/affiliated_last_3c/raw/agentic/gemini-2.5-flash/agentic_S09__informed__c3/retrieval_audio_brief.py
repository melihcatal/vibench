import os
from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv() # Load environment variables

def generate_audio_brief(text: str, output_filepath: str = "brief.mp3") -> str:
    """
    Generates an audio brief (speech) from the given text using Google Cloud Text-to-Speech.
    
    Args:
        text: The text content to convert to speech.
        output_filepath: The path where the generated MP3 audio file will be saved.
                         Defaults to "brief.mp3".
                         
    Returns:
        The filepath of the generated audio file.
    """
    # Google Cloud Text-to-Speech uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure this environment variable points to your service account key file.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Audio generation might fail without proper authentication.")

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or FEMALE, MALE
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        return output_filepath
    except Exception as e:
        print(f"Error generating audio with Google Cloud Text-to-Speech: {e}")
        return f"Error: {e}"

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    # brief_text = "Here is your daily brief from the retrieved search results. " \
    #              "The top result indicates significant progress in renewable energy. " \
    #              "Another important finding highlights new advancements in quantum computing research."
    #
    # audio_file = generate_audio_brief(brief_text, "daily_brief.mp3")
    # print(f"Audio brief generated at: {audio_file}")
    # print("You can now play 'daily_brief.mp3' to hear the brief.")
    pass
