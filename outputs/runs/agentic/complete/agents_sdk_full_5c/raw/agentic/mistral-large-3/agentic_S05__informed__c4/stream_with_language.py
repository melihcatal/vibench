from dashscope import SpeechRecognizer
from speech_client import get_dashscope_client
from partial_results import PartialResultHandler

class LanguageAwareStream:
    def __init__(self, language: str = "zh", enable_punctuation: bool = True):
        self.language = language
        self.enable_punctuation = enable_punctuation
        self.handler = PartialResultHandler()
        self.recognizer = self._setup_recognizer()

    def _setup_recognizer(self) -> SpeechRecognizer:
        recognizer = SpeechRecognizer(
            model="paraformer-realtime-v1",
            format="pcm",
            sample_rate=16000,
            callback=self.handler.handle,
            language=self.language,
            enable_inverse_text_normalization=True,
            enable_punctuation=self.enable_punctuation
        )
        return recognizer

    def send_audio(self, audio_chunk: bytes):
        self.recognizer.stream_send(audio_chunk)

    def close(self):
        self.recognizer.stream_close()

    def get_current_transcript(self) -> str:
        return self.handler.get_current_transcript()

    def get_final_transcripts(self) -> list[str]:
        return self.handler.get_final_transcripts()