from speech_client import create_speech_sdk, normalize_locale


def select_voice(locale: str):
    speechsdk, speech_config = create_speech_sdk()
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    voices = synthesizer.get_voices_async(normalize_locale(locale)).get()
    return [v.name for v in voices.voices]
