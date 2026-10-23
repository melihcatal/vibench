from assemblyai import TranscriptionConfig


def get_basic_config():
    return TranscriptionConfig(
        punctuate=True,
        format_text=True,
    )


def get_diarize_config():
    return TranscriptionConfig(
        speaker_labels=True,
        punctuate=True,
        format_text=True,
    )
