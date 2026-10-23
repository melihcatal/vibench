from google.cloud import texttospeech
import os

def list_voices(language_code: str = None):
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    If no language_code is provided, lists all available voices.
    """
    client = texttospeech.TextToSpeechClient()

    response = client.list_voices(language_code=language_code)

    print(f"Available voices (language_code: {language_code if language_code else 'all'}):")
    for voice in response.voices:
        print(f"  Name: {voice.name}, Supported languages: {voice.language_codes}, Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")

def select_voice_by_criteria(language_code: str, ssml_gender: texttospeech.SsmlVoiceGender, sample_rate_hertz: int = None):
    """
    Selects a voice based on specific criteria.
    """
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)

    for voice in response.voices:
        if voice.language_codes and language_code in voice.language_codes and voice.ssml_gender == ssml_gender:
            if sample_rate_hertz is None or (voice.natural_sample_rate_hertz and voice.natural_sample_rate_hertz == sample_rate_hertz):
                print(f"Selected voice: Name={voice.name}, Gender={texttospeech.SsmlVoiceGender(voice.ssml_gender).name}, Languages={voice.language_codes}")
                return voice.name
    print(f"No voice found matching criteria: language_code={language_code}, gender={ssml_gender.name}")
    return None


if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    print("Listing all English (US) voices:")
    list_voices(language_code="en-US")

    print("\nAttempting to select a female voice for en-US:")
    selected = select_voice_by_criteria(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    if selected:
        print(f"Selected voice for synthesis: {selected}")
