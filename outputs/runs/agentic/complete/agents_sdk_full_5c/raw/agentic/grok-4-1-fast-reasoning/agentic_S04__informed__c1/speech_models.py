import assemblyai as aai

def base_config(speaker_labels=False, punctuate=True, format_text=True):
    return aai.TranscriptionConfig(
        speaker_labels=speaker_labels,
        punctuate=punctuate,
        format_text=format_text,
        language_code="en",
    )