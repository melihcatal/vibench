from google.cloud import texttospeech_v1 as texttospeech
from speech_client import SpeechClient
from typing import List, Dict


def list_voices(language_code: str = None) -> List[Dict]:
    client = SpeechClient().get_client()
    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )

    return voices


def select_voice(
    language_code: str, voice_name: str = None, ssml_gender: str = None
) -> Dict:
    voices = list_voices(language_code)

    for voice in voices:
        if voice_name and voice["name"] != voice_name:
            continue
        if (
            ssml_gender
            and texttospeech.SsmlVoiceGender[voice["ssml_gender"]].name != ssml_gender
        ):
            continue
        return voice

    raise ValueError("No matching voice found")
