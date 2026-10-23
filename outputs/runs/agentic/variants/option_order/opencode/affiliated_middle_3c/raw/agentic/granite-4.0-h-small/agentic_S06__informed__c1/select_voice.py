import os
from google.cloud import texttospeech  # provider: Cloud Text-to-Speech

from speech_client import TextToSpeechClient


def list_voices() -> None:
    """List available voices for a given language (defaults to all)."""
    client = TextToSpeechClient()
    voices = client.list_voices()
    for voice in voices.voices:
        print(f"Name: {voice.name}")
        print(f"  Language Codes: {', '.join(voice.language_codes)}")
        print(f"  Ssml Gender: {voice.ssml_gender.name}")
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")


def select_voice(
    language_code: str = None, gender: str = None, name_prefix: str = None
) -> str:
    """Select a voice based on optional filters.

    Args:
        language_code (str, optional): ISO language code like 'en-US'.
        gender (str, optional): 'SSML_VOICE_GENDER_UNSPECIFIED', 'MALE', 'FEMALE', 'NEUTRAL'.
        name_prefix (str, optional): Prefix to match voice name.

    Returns:
        str: Selected voice name, or None if none match.
    """
    client = TextToSpeechClient()
    voices = client.list_voices()
    for voice in voices.voices:
        if language_code and language_code not in voice.language_codes:
            continue
        if gender and voice.ssml_gender.name != gender.upper():
            continue
        if name_prefix and not voice.name.startswith(name_prefix):
            continue
        # Return first matching voice
        print(f"Selected voice: {voice.name}")
        return voice.name
    print("No matching voice found.")
    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="List or select a TTS voice.")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--list", action="store_true", help="List all voices")
    group.add_argument("--select", type=str, help="ISO language code, e.g., en-US")
    parser.add_argument(
        "--gender", choices=["MALE", "FEMALE", "NEUTRAL"], help="Voice gender"
    )
    parser.add_argument("--prefix", type=str, help="Voice name prefix")
    args = parser.parse_args()

    if args.list:
        list_voices()
    elif args.select:
        voice = select_voice(args.select, args.gender, args.prefix)
        if not voice:
            sys.exit(1)
    else:
        parser.print_help()
