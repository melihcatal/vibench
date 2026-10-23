from google.cloud import texttospeech

def list_voices(locale: str) -> list[dict]:
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_codes=[locale])
    return [
        {
            "name": voice.name,
            "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else None,
            "language_codes": voice.language_codes
        }
        for voice in response.voices
    ]

def select_voice(locale: str, preferred_gender: str = None) -> str | None:
    voices = list_voices(locale)
    if preferred_gender:
        for voice_dict in voices:
            if voice_dict["ssml_gender"] == preferred_gender:
                return voice_dict["name"]
    return voices[0]["name"] if voices else None