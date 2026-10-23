
from google.cloud import texttospeech

def generate_spoken_brief(brief_text: str, output_filepath: str):
    """
    Generates a spoken brief from the given text using Google Cloud Text-to-Speech.

    Args:
        brief_text: The text content of the brief.
        output_filepath: The path to save the generated audio file (e.g., "brief.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Configure the voice (e.g., US English, Wavenet-A voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-A",  # Google Cloud Text-to-Speech specific voice identifier
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to the output file
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

if __name__ == "__main__":
    # Example usage:
    example_brief = "Reviewer, a new audio submission needs your attention. It is categorized as a potential hate speech violation. Please review it carefully and take appropriate action."
    output_file = "moderation_brief.mp3"
    generate_spoken_brief(example_brief, output_file)
