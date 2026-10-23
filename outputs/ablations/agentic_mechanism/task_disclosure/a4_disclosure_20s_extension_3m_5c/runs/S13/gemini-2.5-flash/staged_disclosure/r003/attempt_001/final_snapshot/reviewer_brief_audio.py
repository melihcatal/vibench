
from google.cloud import texttospeech

def generate_audio_brief(text_content, output_filename="reviewer_brief.mp3"):
    """Generates an audio brief from text content using Google Cloud Text-to-Speech.

    Args:
        text_content (str): The text to be converted to speech.
        output_filename (str): The name of the output MP3 file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Configure the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",  # A standard US English voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio output format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to a file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'''Audio content written to file "{output_filename}"''')

if __name__ == "__main__":
    brief_text = "This is a brief for the moderation reviewer. The content requires urgent attention due to potential policy violations. Please review carefully."
    generate_audio_brief(brief_text)
