from google.cloud import speech_v1p1beta1 as speech

def create_batch_recognize_config(language_code: str = 'en-US', enable_automatic_punctuation: bool = True):
    """Creates a RecognitionConfig for batch transcription."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Common for WAV/PCM
        sample_rate_hertz=16000, # Example sample rate, adjust as needed
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    return config

def create_diarization_config(language_code: str = 'en-US', enable_automatic_punctuation: bool = True, 
                            enable_speaker_diarization: bool = True, min_speaker_count: int = 2, max_speaker_count: int = 6):
    """Creates a RecognitionConfig for batch transcription with speaker diarization."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, 
        sample_rate_hertz=16000, 
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        diarization_config=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=enable_speaker_diarization,
            min_speaker_count=min_speaker_count,
            max_speaker_count=max_speaker_count,
        ),
    )
    return config

def create_word_timestamp_config(language_code: str = 'en-US', enable_automatic_punctuation: bool = True, enable_word_time_offsets: bool = True):
    """Creates a RecognitionConfig for batch transcription with word timestamps."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, 
        sample_rate_hertz=16000, 
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
    )
    return config

def create_recognition_audio(gcs_uri: str):
    """Creates a RecognitionAudio object from a GCS URI."""
    audio = speech.RecognitionAudio(uri=gcs_uri)
    return audio
