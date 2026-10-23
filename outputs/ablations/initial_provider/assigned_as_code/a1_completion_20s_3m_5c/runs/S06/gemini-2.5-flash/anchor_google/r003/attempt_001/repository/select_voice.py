from google.cloud import texttospeech


def select_voice(language_code="en-US", gender=None):
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices

    selected_voices = []
    for voice in voices:
        if gender is None or texttospeech.SsmlVoiceGender(gender).name == voice.ssml_gender.name:
            selected_voices.append({
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": voice.ssml_gender.name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            })
    return {"voices": selected_voices}
