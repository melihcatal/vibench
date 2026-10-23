import os
import azure.cognitiveservices.speech as speechsdk


def list_voices(locale_filter=None):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    result = synthesizer.get_voices_async().get()

    voices = []
    for voice in result.voices:
        voice_info = {
            "name": voice.short_name,
            "locale": voice.locale,
            "gender": voice.gender.name if voice.gender else "Unknown",
            "voice_type": voice.voice_type.name if voice.voice_type else "Unknown",
        }

        if locale_filter:
            if voice.locale.startswith(locale_filter):
                voices.append(voice_info)
        else:
            voices.append(voice_info)

    return voices


def select_voice_for_locale(locale, gender_preference=None):
    voices = list_voices(locale)

    if not voices:
        raise ValueError(f"No voices found for locale: {locale}")

    if gender_preference:
        filtered_voices = [
            v for v in voices if v["gender"].lower() == gender_preference.lower()
        ]
        if filtered_voices:
            voices = filtered_voices

    neural_voices = [v for v in voices if "neural" in v["name"].lower()]
    if neural_voices:
        return neural_voices[0]["name"]

    return voices[0]["name"]


def get_voice_details(voice_name):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    result = synthesizer.get_voices_async().get()

    for voice in result.voices:
        if voice.short_name == voice_name:
            return {
                "name": voice.short_name,
                "locale": voice.locale,
                "gender": voice.gender.name if voice.gender else "Unknown",
                "voice_type": voice.voice_type.name if voice.voice_type else "Unknown",
                "supported_styles": voice.style_list
                if hasattr(voice, "style_list")
                else [],
            }

    raise ValueError(f"Voice not found: {voice_name}")
