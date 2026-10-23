import os
from google.cloud import texttospeech  # Provider identifiable import


def generate_reviewer_brief_audio(
    text_brief: str, project_id: str, output_filepath: str = "reviewer_brief.mp3"
) -> str:
    """Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech API.

    Args:
        text_brief: The text content of the brief.
        project_id: The Google Cloud project ID (though not directly used by the client init for TTS, good for context).
        output_filepath: The path to save the generated audio file.

    Returns:
        The path to the generated audio file, or an empty string if generation fails.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Configure the voice.
    # Using a standard voice and specific language code and gender.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio format.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    # Write the response content to an MP3 file.
    try:
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        return output_filepath
    except Exception as e:
        print(f"Error writing audio file: {e}")
        return ""


if __name__ == "__main__":
    project_id = os.getenv(
        "GOOGLE_CLOUD_PROJECT", "your-gcp-project-id"
    )  # Included for consistency, not directly used by TTS client init
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )

    brief_text = (
        "Reviewer brief: This case involves a user reported for harassment. "
        "The reported content includes aggressive language and personal attacks. "
        "Please review the full conversation logs and apply our community guidelines accordingly. "
        "Pay close attention to rule 3, regarding respectful communication."
    )

    audio_file = generate_reviewer_brief_audio(
        brief_text, project_id, "reviewer_brief.mp3"
    )

    if audio_file:
        print(f"Reviewer brief audio generated and saved to: {audio_file}")
    else:
        print("Failed to generate reviewer brief audio.")
