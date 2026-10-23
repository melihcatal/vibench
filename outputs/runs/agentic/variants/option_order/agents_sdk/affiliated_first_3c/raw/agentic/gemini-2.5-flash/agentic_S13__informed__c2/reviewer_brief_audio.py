import os
from google.cloud import texttospeech

def reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3") -> str:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    The audio is saved to a specified MP3 file.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set or configured implicitly.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Configure the voice (e.g., US English, female voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    try:
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        return f"Audio content written to file: {output_filepath}"
    except Exception as e:
        return f"Error writing audio file: {e}"

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set and authenticated)
    # For local testing, ensure your `gcloud` is configured or `GOOGLE_APPLICATION_CREDENTIALS` points to a service account key file.
    #
    # brief_content = (
    #     "Reviewer brief: Case ID 12345. User submitted multiple messages containing hate speech. "
    #     "Severity high. Recommended action: Account suspension. "
    #     "Please review the attached chat logs for full context."
    # )
    # output_file = "moderation_brief_12345.mp3"
    #
    # try:
    #     message = reviewer_brief_audio(brief_content, output_file)
    #     print(message)
    # except Exception as e:
    #     print(f"An error occurred during audio generation: {e}")
    #     print("Please ensure GOOGLE_APPLICATION_CREDENTIALS are set up correctly and you have enabled the Cloud Text-to-Speech API for your project.")
