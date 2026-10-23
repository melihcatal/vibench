import os
from google.cloud import texttospeech

def generate_audio_brief(text: str, output_filename: str = "brief.mp3"):
    """
    Generates an audio brief from the given text using Google Cloud Text-to-Speech.

    Args:
        text: The text content for the audio brief.
        output_filename: The name of the output audio file (e.g., "brief.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
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
    brief_text = "This is a brief for the moderation reviewer. The user submitted a message about a policy violation regarding offensive language. Please review the flagged content and take appropriate action."
    generate_audio_brief(brief_text, "moderation_brief.mp3")
