from google.cloud import texttospeech


def list_voices(language_code: str = "en-US") -> list[dict]:
    client = texttospeech.TextToSpeechClient()
    parent = f"projects/{client._credentials.project_id or 'global'}/locations/global"
    voices = client.list_voices(parent=parent)
    filtered_voices = [v for v in voices.voices if language_code in v.language_codes]
    return [
        {
            "name": v.name.split("/")[-1],
            "gender": v.gender.name,
            "language_codes": v.language_codes,
        }
        for v in filtered_voices
    ]


def select_voice(language_code: str = "en-US", gender: str = "FEMALE") -> str:
    voices = list_voices(language_code)
    for voice in voices:
        if voice["gender"] == gender:
            return voice["name"]
    return voices[0]["name"] if voices else None
