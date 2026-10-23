import os
from google.cloud import texttospeech

def reviewer_brief_audio(text_brief: str, output_audio_path: str = "brief.mp3") -> str:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    Saves the audio to a specified file path.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or explicitly pass credentials to the TextToSpeechClient constructor.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Or MALE/FEMALE
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Write the audio content to a file
        with open(output_audio_path, "wb") as out:
            out.write(response.audio_content)
        return f"Audio content written to '{output_audio_path}'"

    except Exception as e:
        return f"Error generating audio brief: {str(e)}"

if __name__ == "__main__":
    # Example Usage
    # Set GOOGLE_APPLICATION_CREDENTIALS to a service account key file path.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    sample_brief = "Reviewer, please note that the user message contained severe hate speech and violence. The system denied the content automatically. Further human review is recommended to understand the context."
    audio_file = "reviewer_brief.mp3"
    result_message = reviewer_brief_audio(sample_brief, audio_file)
    print(result_message)
