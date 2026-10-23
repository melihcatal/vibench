import os
import sys
from typing import Optional

from google.cloud import texttospeech


def synthesize_ssml(ssml: str, output_path: str, voice_name: Optional[str] = None, language_code: str = "en-US") -> None:
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(ssml=ssml)
    voice_params = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name) if voice_name else texttospeech.VoiceSelectionParams(language_code=language_code)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice_params, audio_config=audio_config)
    with open(output_path, "wb") as f:
        f.write(response.audio_content)


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: synthesize_ssml.py '<ssml>' <output_path> [voice_name] [language_code]", file=sys.stderr)
        return 1
    ssml = sys.argv[1]
    output_path = sys.argv[2]
    voice_name = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
    language_code = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] else "en-US"
    synthesize_ssml(ssml, output_path, voice_name=voice_name, language_code=language_code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
