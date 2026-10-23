import os
from typing import Optional, Union

from google.cloud import texttospeech


def synthesize_ssml(
    ssml: str,
    voice_name: str,
    language_code: str,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    output_path: Optional[str] = None,
) -> Union[bytes, str]:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    if output_path:
        with open(output_path, "wb") as f:
            f.write(response.audio_content)
        return output_path
    return response.audio_content
