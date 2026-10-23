from google.cloud import texttospeech
import os

def generate_audio_brief(brief_text: str, output_filename: str = "reviewer_brief.mp3"):
    """
    Generates a spoken audio brief from the given text using Google Cloud Text-to-Speech.

    Args:
        brief_text: The text content of the brief.
        output_filename: The name of the output audio file (e.g., "reviewer_brief.mp3").
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input with the plain text to be synthesized.
    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The audio content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS environment variable set
    # or authenticate otherwise for Google Cloud.
    # For more information: https://cloud.google.com/docs/authentication/getting-started
    
    # Example brief text for a moderation reviewer
    brief = """
    Hello reviewer. This is an audio brief for the next moderation task.
    Please review the content submitted by user ID 12345 for potential violations
    of our community guidelines, specifically regarding hate speech and harassment.
    The content in question is a comment posted on a public forum.
    Pay close attention to the tone and specific phrases used.
    Thank you.
    """
    generate_audio_brief(brief, "moderation_brief_12345.mp3")
