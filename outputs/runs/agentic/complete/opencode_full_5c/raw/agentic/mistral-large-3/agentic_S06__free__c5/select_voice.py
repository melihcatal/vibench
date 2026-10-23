from google.cloud import texttospeech_v1 as tts
from speech_client import TextToSpeechClient
from typing import List, Dict


def list_voices(language_code: str = None) -> List[Dict]:
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = TextToSpeechClient().get_client()

    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": tts.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )

    return voices


def select_voice(
    language_code: str, voice_name: str = None, ssml_gender: str = None
) -> Dict:
    """
    Selects a voice for a target locale using Google Cloud Text-to-Speech.
    """
    voices = list_voices(language_code)

    if voice_name:
        voices = [v for v in voices if v["name"] == voice_name]

    if ssml_gender:
        voices = [v for v in voices if v["ssml_gender"] == ssml_gender]

    if not voices:
        raise ValueError("No matching voice found")

    return voices[0]
