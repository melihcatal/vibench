# Generate spoken briefs for moderation reviewers
from google.cloud import texttospeech_v1 as tts


def generate_reviewer_brief(text: str, output_file: str) -> None:
    """Generate spoken brief using Google Cloud Text-to-Speech API."""
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D"
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)