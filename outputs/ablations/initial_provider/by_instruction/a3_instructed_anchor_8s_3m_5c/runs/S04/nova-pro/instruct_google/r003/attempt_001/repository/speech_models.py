from google.cloud import speech_v1p1beta1 as speech

def create_recognition_config(encoding: str, sample_rate_hertz: int, language_code: str, enable_automatic_punctuation: bool = True, enable_word_time_offsets: bool = True, enable_speaker_diarization: bool = False, diarization_speaker_count: int = 0) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=getattr(speech.RecognitionConfig.AudioEncoding, encoding),
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        enable_speaker_diarization=enable_speaker_diarization,
        diarization_speaker_count=diarization_speaker_count
    )