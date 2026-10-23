import os
from google.cloud import texttospeech

def reviewer_brief_audio(text: str, output_filepath: str = "brief_audio.mp3") -> str:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set for authentication.
    """
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable must be set for Google Cloud Text-to-Speech.")

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

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
        return f"Audio content written to file {output_filepath}"
    except Exception as e:
        return f"Error generating speech: {e}"

if __name__ == '__main__':
    # Example usage - ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # brief_text = "This is a brief for a moderation case. The user appealed a decision regarding hate speech."
    # print(reviewer_brief_audio(brief_text, "case_brief_123.mp3"))
    pass
