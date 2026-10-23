import os
import google.cloud.texttospeech as tts

# Helper utilities are imported from local modules
from speech_client import get_texttospeech_client
from speech_models import voice_to_dict

def list_voices(language_code: str = None) -> list[dict]:
    """List available voices and optionally filter by a language code.

    Args:
        language_code (str, optional): BCP-47 language code (e.g., "en-US"). If None,
            all voices are returned.

    Returns:
        List of dicts with keys: name, language_codes, gender, natural_sample_rate_Hz.
    """
    client = get_texttospeech_client()
    response = client.list_voices(language_code=language_code)

    voices = []
    for v in response.voices:
        voice_info = {
            "name": v.name,
            "language_codes": v.language_codes,
            "gender": v.ssml_gender.name,
            "natural_sample_rate_Hz": v.natural_sample_rate_hertz,
        }
        voices.append(voice_info)
    return voices

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     voices = list_voices("en-US")
#     for v in voices:
#         print(v)
