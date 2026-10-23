import os
from google.cloud import texttospeech


def generate_reviewer_brief_audio(
    text: str, output_filepath: str = "reviewer_brief.mp3"
):
    """
    Generates spoken audio briefs for moderation reviewers using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up (e.g., via service account key file).
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice selection
    # You can choose a different voice by changing language_code and name
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Audio config
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary. We can save it to a file.
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        return {"text": text, "audio_filepath": output_filepath, "status": "success"}
    except Exception as e:
        return {"error": str(e)}
