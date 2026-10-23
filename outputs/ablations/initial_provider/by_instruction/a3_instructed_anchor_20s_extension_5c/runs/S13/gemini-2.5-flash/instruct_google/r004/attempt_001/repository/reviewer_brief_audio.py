from google.cloud import texttospeech
import os

def reviewer_brief_audio(text: str, output_filepath: str, project_id: str = None) -> None:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice selection
    # You can customize the language code and voice name as needed.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        name="en-US-Wavenet-D" # A common high-quality voice
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    print(f"Audio content written to file: {output_filepath}")
