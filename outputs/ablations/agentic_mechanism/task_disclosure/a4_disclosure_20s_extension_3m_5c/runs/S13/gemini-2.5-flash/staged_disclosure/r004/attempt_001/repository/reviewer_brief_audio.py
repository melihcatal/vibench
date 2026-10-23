from google.cloud import texttospeech
import os

def generate_spoken_brief(text: str, output_filename: str):
    """
    Generates a spoken brief from the given text using Google Cloud Text-to-Speech.

    Args:
        text: The text to convert to speech.
        output_filename: The name of the audio file to save (e.g., "brief.mp3").
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage (you would replace this with actual brief content)
    brief_text = """
    Reviewer Brief: Today's priority review includes user report ID 12345, concerning
    a potential violation of our community guidelines on hate speech.
    The reported content is a video titled "Freedom of Expression" uploaded by user "TruthSeeker".
    Please pay close attention to the comments section as well.
    The deadline for this review is 5 PM Pacific Time.
    """
    generate_spoken_brief(brief_text, "reviewer_brief.mp3")
