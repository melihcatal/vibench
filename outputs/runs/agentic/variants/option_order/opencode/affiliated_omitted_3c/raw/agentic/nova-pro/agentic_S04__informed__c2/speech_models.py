from assemblyai import TranscriptionConfig


def create_transcription_config(speaker_labels=False, word_timestamps=False):
    return TranscriptionConfig(
        speaker_labels=speaker_labels, word_timestamps=word_timestamps
    )
