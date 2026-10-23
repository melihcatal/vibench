import os
from google.cloud import texttospeech

def reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3") -> str:
    """Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.

    Args:
        brief_text: The text for the reviewer brief.
        output_filepath: The path where the generated audio file will be saved.

    Returns:
        The path to the generated audio file, or an error message if failed.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # default authentication is configured for Google Cloud.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or FEMALE/MALE
    )

    # Configure the audio output format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # The response's audio_content is binary. Write it to an MP3 file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file: {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"Error generating audio brief with Google Cloud Text-to-Speech: {e}")
        return f"Error generating audio: {e}"

if __name__ == "__main__":
    # Example usage (requires Google Cloud credentials set up, e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    # brief = (
    #     "Review case #12345. The user submitted content that was flagged for severe hate speech."
    #     "Recommended action is a temporary ban. Please verify the context and apply policy."
    # )
    # audio_file = reviewer_brief_audio(brief, "moderation_brief_12345.mp3")
    # print(f"Generated audio file: {audio_file}")
    pass
