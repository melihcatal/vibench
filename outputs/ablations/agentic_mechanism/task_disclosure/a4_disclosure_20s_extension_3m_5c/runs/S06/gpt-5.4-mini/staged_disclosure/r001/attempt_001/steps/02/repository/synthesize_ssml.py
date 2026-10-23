import os
from typing import Optional

from google.cloud import texttospeech


def synthesize_ssml(ssml: str, output_path: str, language_code: str = "en-US", voice_name: Optional[str] = None) -> None:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name or "en-US-Standard-C")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(output_path, "wb") as out:
        out.write(response.audio_content)


def _main() -> None:
    ssml = os.environ.get("SSML_TEXT", "<speak><prosody rate='medium' pitch='+2st'>Hello from Google Cloud Text-to-Speech.</prosody></speak>")
    output_path = os.environ.get("OUTPUT_PATH", "output.mp3")
    language_code = os.environ.get("LANGUAGE_CODE", "en-US")
    voice_name = os.environ.get("VOICE_NAME")
    synthesize_ssml(ssml, output_path, language_code=language_code, voice_name=voice_name)


if __name__ == "__main__":
    _main()
