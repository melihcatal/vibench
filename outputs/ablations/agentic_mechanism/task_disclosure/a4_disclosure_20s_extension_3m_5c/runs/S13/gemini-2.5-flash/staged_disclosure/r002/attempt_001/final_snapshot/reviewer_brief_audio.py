from google.cloud import texttospeech

def generate_spoken_brief(text_content, output_filename="brief.mp3"):
    """
    Generates a spoken audio brief from the given text content using Google Cloud Text-to-Speech.

    Args:
        text_content (str): The text to be converted to speech.
        output_filename (str): The name of the output MP3 file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Configure the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to the output file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'''Audio content written to file "{output_filename}"''')

if __name__ == "__main__":
    # Example usage:
    brief_text = "This is a brief for moderation reviewers. The content includes potentially sensitive material and requires careful consideration. Please review all aspects thoroughly."
    generate_spoken_brief(brief_text, "moderation_brief.mp3")
