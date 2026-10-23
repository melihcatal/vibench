from speech_client import tts_client


def select_voice(locale="en-US"):
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    return [voice for voice in voices if locale.startswith("en")]
