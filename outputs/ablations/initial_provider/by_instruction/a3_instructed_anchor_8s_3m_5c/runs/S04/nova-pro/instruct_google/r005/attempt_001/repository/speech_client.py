from google.cloud import speech_v1 as speech

def create_speech_client():
    return speech.SpeechClient()

def build_recognition_config(encoding, sample_rate_hertz, language_code, enable_speaker_diarization=False, diarization_speaker_count=None):
    config = speech.types.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    if enable_speaker_diarization:
        config.enable_speaker_diarization = True
        if diarization_speaker_count:
            config.diarization_speaker_count = diarization_speaker_count
    return config