from assemblyai import TranscriptionConfig


def basic_config():
    return TranscriptionConfig(punctuate=True, format_text=True)


def diarized_config():
    config = basic_config()
    config.speaker_labels = True
    return config
