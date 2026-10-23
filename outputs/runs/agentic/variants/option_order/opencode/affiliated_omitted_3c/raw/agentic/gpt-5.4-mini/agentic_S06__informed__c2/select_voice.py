from typing import List, Optional

from speech_client import make_polly_client, voice_options_from_polly


def select_voice(locale: Optional[str] = None) -> List[dict]:
    client = make_polly_client()
    response = (
        client.describe_voices(LanguageCode=locale)
        if locale
        else client.describe_voices()
    )
    return [
        voice.__dict__ for voice in voice_options_from_polly(response.get("Voices", []))
    ]
