from typing import Dict, Any, List


class TranscriptionRequest:
    def __init__(
        self,
        audio_url: str,
        enable_diarization: bool = False,
        enable_timestamps: bool = False,
    ):
        self.audio_url = audio_url
        self.enable_diarization = enable_diarization
        self.enable_timestamps = enable_timestamps

    def to_assemblyai_config(self) -> Dict[str, Any]:
        return {
            "speaker_diarization": self.enable_diarization,
            "word_timestamps": self.enable_timestamps,
            "language_code": "en_us",
        }


class TranscriptionResponse:
    def __init__(self, raw_response: Any):
        self.raw_response = raw_response

    def get_text(self) -> str:
        return self.raw_response.text

    def get_words(self) -> List[Dict[str, Any]]:
        if hasattr(self.raw_response, "words"):
            return [
                {"text": word.text, "start": word.start, "end": word.end}
                for word in self.raw_response.words
            ]
        return []

    def get_speakers(self) -> List[Dict[str, Any]]:
        if hasattr(self.raw_response, "utterances"):
            return [
                {"speaker": utterance.speaker, "text": utterance.text}
                for utterance in self.raw_response.utterances
            ]
        return []
