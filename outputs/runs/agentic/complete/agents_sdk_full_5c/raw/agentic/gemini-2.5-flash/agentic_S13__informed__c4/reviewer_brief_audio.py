import os
from google.cloud import textto_speech_v1 as texttospeech

def generate_reviewer_brief_audio(text: str, output_filepath: str = "reviewer_brief.mp3"):
    """
    Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Text-to-Speech might fail.")

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice (e.g., standard US English female)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-A", # A standard voice. Other options like Wavenet.
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
        return output_filepath
    except Exception as e:
        print(f"Error generating speech with Google Cloud Text-to-Speech: {e}")
        return None
