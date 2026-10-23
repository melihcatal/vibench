import os
from google.cloud import texttospeech
from typing import Dict, Any

def reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3") -> str:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or FEMALE, MALE
    )

    # Configure the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    
    return f"Audio content written to file: {output_filepath}"

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS or gcloud auth to be configured)
    # brief_content = "This is a brief for the moderation reviewer. Case ID 123 involves severe hate speech. Please prioritize review."
    # output_file = "moderation_brief_123.mp3"
    # result_message = reviewer_brief_audio(brief_content, output_file)
    # print(result_message)
    pass
