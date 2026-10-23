from google.cloud import texttospeech_v1


def generate_reviewer_brief_audio(text: str, output_filepath: str) -> None:
    """Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech API."""
    client = texttospeech_v1.TextToSpeechClient()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    # Configure the voice (e.g., US English, female voice)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
    )

    # Configure the audio output (e.g., MP3)
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
