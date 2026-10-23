from google.cloud import texttospeech


def select_voice(language_code="en-US", config=None):
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices
    
    # You can add more sophisticated logic here to filter or select a specific voice
    # For now, let's return a list of voice names and genders
    return [
        {
            "name": voice.name,
            "language_codes": voice.language_codes,
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }
        for voice in voices
    ]