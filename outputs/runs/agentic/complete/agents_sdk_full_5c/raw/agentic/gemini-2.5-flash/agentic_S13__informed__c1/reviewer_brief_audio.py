import os
from google.cloud import texttospeech

def generate_reviewer_brief_audio(text: str, output_filepath: str) -> None:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    """
    # Google Cloud Text-to-Speech client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # that your environment is otherwise authenticated for Google Cloud.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Concrete model aspect
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filepath}" for review.')

if __name__ == '__main__':
    # Example usage
    # Set environment variable GOOGLE_APPLICATION_CREDENTIALS pointing to your service account key file
    # For instance:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    sample_brief_text = (
        "Review case number 12345. User submitted content contained severe hate speech."
        "The decision was to remove the content and issue a 24-hour ban."
        "Further details are available in the attached moderation log."
    )
    output_file = "reviewer_brief.mp3"

    try:
        generate_reviewer_brief_audio(sample_brief_text, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")
