from google.cloud import texttospeech
from .speech_client import TextToSpeechClient

client = TextToSpeechClient()

def list_voices(language_code: str = None):
    voices = client.list_voices(language_code=language_code)
    for voice in voices.voices:
        print(f"Name: {voice.name}, Language: {voice.language_codes[0]}, Gender: {voice.ssml_gender}")

def select_voice(language_code: str = None, gender: str = None):
    voices = client.list_voices(language_code=language_code)
    matches = []
    for voice in voices.voices:
        if language_code and voice.language_codes[0] != language_code:
            continue
        if gender and voice.ssml_gender.name() != gender.upper():
            continue
        matches.append(voice)
    if matches:
        return matches[0].name
    return None

if __name__ == "__main__":
    # List all English voices
    list_voices("en")

    # Select a male British English voice
    voice_name = select_voice(language_code="en-GB", gender="MALE")
    print("Selected voice name:", voice_name)
