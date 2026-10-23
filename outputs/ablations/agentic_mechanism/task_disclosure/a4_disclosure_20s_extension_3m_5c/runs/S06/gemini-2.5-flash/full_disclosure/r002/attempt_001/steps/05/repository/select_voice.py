from google.cloud import texttospeech

def list_voices_by_locale(language_code: str = None):
    """Lists the available voices, optionally filtered by language code.

    Args:
        language_code: The BCP-47 language code to filter voices by (e.g., "en-US").

    Returns:
        A list of voice names and their supported language codes.
    """
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices

    filtered_voices = []
    for voice in voices:
        if language_code:
            for lang in voice.language_codes:
                if lang == language_code:
                    filtered_voices.append(
                        {
                            "name": voice.name,
                            "language_codes": voice.language_codes,
                            "ssml_gender": voice.ssml_gender.name,
                            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                        }
                    )
                    break
        else:
            filtered_voices.append(
                {
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": voice.ssml_gender.name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                }
            )
    return filtered_voices

def select_voice(language_code: str, ssml_gender: str = None):
    """Selects a voice for a target locale and optional gender.

    Args:
        language_code: The BCP-47 language code (e.g., "en-US").
        ssml_gender: The SSML voice gender ("MALE", "FEMALE", "NEUTRAL").

    Returns:
        A selected voice name, or None if no matching voice is found.
    """
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices

    for voice in voices:
        if language_code in voice.language_codes:
            if ssml_gender is None or voice.ssml_gender.name == ssml_gender.upper():
                return voice.name
    return None