import os
from google.cloud import texttospeech

def generate_reviewer_brief_audio(text_brief: str, output_file_path: str = "reviewer_brief.mp3") -> str:
    """Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech."""
    # Google Cloud Text-to-Speech uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure this environment variable is set or ADC is configured.
    # The client will automatically pick up credentials from the environment.

    client = texttospeech.TextToSpeechClient()

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Defaulting to Application Default Credentials setup.")

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Configure the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Write the response audio content to the output file
        with open(output_file_path, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file '{output_file_path}'")
        return output_file_path
    except Exception as e:
        print(f"Error generating audio brief with Google Cloud Text-to-Speech: {e}")
        raise
