from google.cloud import texttospeech

def list_voices_for_locale(language_code: str = "en-US"):
    """Lists available voices for a specific locale using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append({
            "name": voice.name,
            "language_codes": voice.language_codes,
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.sample_rate_hertz,
        })
    return voice_list

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # us_voices = list_voices_for_locale("en-US")
    # print("Available en-US voices:")
    # for voice in us_voices[:5]: # Print first 5 for brevity
    #     print(f"  Name: {voice['name']}, Gender: {voice['ssml_gender']}")
    pass
