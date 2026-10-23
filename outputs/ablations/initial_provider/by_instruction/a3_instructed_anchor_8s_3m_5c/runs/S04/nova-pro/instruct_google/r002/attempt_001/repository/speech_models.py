from google.cloud import speech_v1 as speech

def recognition_config(encoding, sample_rate_hertz, language_code, enable_speaker_diarization=False, diarization_speaker_count=0, enable_word_time_offsets=False):
    return speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_speaker_diarization=enable_speaker_diarization,
        diarization_speaker_count=diarization_speaker_count,
        enable_word_time_offsets=enable_word_time_offsets,
    )