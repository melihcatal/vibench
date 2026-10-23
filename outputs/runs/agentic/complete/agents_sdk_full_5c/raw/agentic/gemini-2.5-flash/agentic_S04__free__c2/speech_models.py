from typing import List, Dict, Any

class TranscriptionConfig:
    """Defines configuration for a batch transcription request."""
    def __init__(self, audio_uri: str, language_code: str = "en-US", enable_word_time_offsets: bool = False, enable_speaker_diarization: bool = False, diarization_speaker_count: int = 2):
        self.audio_uri = audio_uri
        self.language_code = language_code
        self.enable_word_time_offsets = enable_word_time_offsets
        self.enable_speaker_diarization = enable_speaker_diarization
        self.diarization_speaker_count = diarization_speaker_count

    def to_recognition_config(self) -> Dict[str, Any]:
        config = {
            "language_code": self.language_code,
            "enable_word_time_offsets": self.enable_word_time_offsets,
            "model": "default", # Use the default model, could be specified as 'latest_long'
            "encoding": "LINEAR16", # Placeholder, typically inferred or provided by user
            "sample_rate_hertz": 16000 # Placeholder, typically inferred or provided by user
        }
        if self.enable_speaker_diarization:
            config["diarization_config"] = {"enable_speaker_diarization": True, "min_speaker_count": 2, "max_speaker_count": self.diarization_speaker_count}
        return config

    def to_recognition_audio(self) -> Dict[str, Any]:
        return {"uri": self.audio_uri}

class TranscriptionResult:
    """Represents the result of a transcription operation."""
    def __init__(self, full_transcript: str, word_timestamps: List[Dict[str, Any]] = None, speaker_segments: List[Dict[str, Any]] = None):
        self.full_transcript = full_transcript
        self.word_timestamps = word_timestamps if word_timestamps is not None else []
        self.speaker_segments = speaker_segments if speaker_segments is not None else []

    def __str__(self):
        return self.full_transcript
