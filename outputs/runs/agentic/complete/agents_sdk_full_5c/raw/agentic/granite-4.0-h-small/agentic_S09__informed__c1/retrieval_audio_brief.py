import os
from google.cloud import texttospeech

def generate_audio_brief(text: str, output_path: str = "brief.mp3") -> None:
    """Synthesize spoken audio from a brief text using Google Cloud Text-to-Speech.",
    client = texttospeech.TextToSpeechClient()
    input_ssml = texttospeech.SynthesisInput(ssml=f"<speak>{text}</speak>")
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio brief written to {output_path}")