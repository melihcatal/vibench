from google.cloud import speech
from typing import Optional, Generator, Dict, Any
import queue
import threading


class LanguageAwareStreamingRecognizer:
    def __init__(self, api_key: Optional[str] = None):
        self.client = speech.SpeechClient()
        self.supported_languages = {
            "en-US": "English (United States)",
            "en-GB": "English (Great Britain)",
            "es-ES": "Spanish (Spain)",
            "fr-FR": "French (France)",
            "de-DE": "German (Germany)",
            "ja-JP": "Japanese (Japan)",
            "ko-KR": "Korean (South Korea)",
            "zh-CN": "Chinese (Mandarin, Simplified)",
            "zh-TW": "Chinese (Mandarin, Traditional)",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian (Russia)",
            "it-IT": "Italian (Italy)",
            "nl-NL": "Dutch (Netherlands)",
            "ar-SA": "Arabic (Saudi Arabia)",
            "hi-IN": "Hindi (India)",
        }

    def create_streaming_config(
        self,
        language_code: str = "en-US",
        enable_automatic_punctuation: bool = True,
        enable_word_confidence: bool = False,
        enable_speaker_diarization: bool = False,
        diarization_speaker_count: int = 2,
        model: str = "latest_long",
        use_enhanced: bool = False,
    ) -> speech.StreamingRecognitionConfig:

        if language_code not in self.supported_languages:
            raise ValueError(
                f"Unsupported language code: {language_code}. Supported: {list(self.supported_languages.keys())}"
            )

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
            enable_word_confidence=enable_word_confidence,
            enable_speaker_diarization=enable_speaker_diarization,
            diarization_config=speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=enable_speaker_diarization,
                min_speaker_count=1,
                max_speaker_count=diarization_speaker_count,
            )
            if enable_speaker_diarization
            else None,
            model=model,
            use_enhanced=use_enhanced,
        )

        return speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
            single_utterance=False,
        )

    def start_streaming_recognizer(
        self,
        audio_stream: Generator[bytes, None, None],
        language_code: str = "en-US",
        **kwargs,
    ) -> Generator[Dict[str, Any], None, None]:

        streaming_config = self.create_streaming_config(
            language_code=language_code, **kwargs
        )

        def request_generator():
            for chunk in audio_stream:
                if chunk:
                    yield speech.StreamingRecognizeRequest(audio_content=chunk)

        responses = self.client.streaming_recognize(
            streaming_config, request_generator()
        )

        for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if not result.alternatives:
                    continue

                alternative = result.alternatives[0]

                yield {
                    "transcript": alternative.transcript,
                    "is_final": result.is_final,
                    "confidence": alternative.confidence,
                    "language_code": language_code,
                    "language_name": self.supported_languages.get(
                        language_code, language_code
                    ),
                    "has_punctuation": kwargs.get("enable_automatic_punctuation", True),
                    "speaker_tag": getattr(result, "speaker_tag", None)
                    if kwargs.get("enable_speaker_diarization", False)
                    else None,
                    "word_confidence": getattr(alternative, "words", [])
                    if kwargs.get("enable_word_confidence", False)
                    else None,
                }

    def stream_with_multilingual_detection(
        self,
        audio_stream: Generator[bytes, None, None],
        possible_languages: list = None,
    ) -> Generator[Dict[str, Any], None, None]:

        if possible_languages is None:
            possible_languages = ["en-US", "es-ES", "fr-FR", "de-DE"]

        for lang_code in possible_languages:
            if lang_code in self.supported_languages:
                try:
                    for result in self.start_streaming_recognizer(
                        audio_stream, language_code=lang_code
                    ):
                        result["detected_language"] = lang_code
                        yield result
                    break
                except Exception as e:
                    print(f"Failed with language {lang_code}: {e}")
                    continue

    def create_realtime_stream(self, sample_rate: int = 16000, chunk_size: int = 1024):
        import pyaudio

        audio_queue = queue.Queue()

        def audio_callback(in_data, frame_count, time_info, status):
            audio_queue.put(in_data)
            return (in_data, pyaudio.paContinue)

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size,
            stream_callback=audio_callback,
        )

        def audio_generator():
            stream.start_stream()
            try:
                while True:
                    chunk = audio_queue.get()
                    if chunk is None:
                        break
                    yield chunk
            finally:
                stream.stop_stream()
                stream.close()
                p.terminate()

        return audio_generator()


def example_usage():
    recognizer = LanguageAwareStreamingRecognizer()

    audio_gen = recognizer.create_realtime_stream()

    print("Starting English streaming recognition with punctuation...")
    for result in recognizer.start_streaming_recognizer(
        audio_gen,
        language_code="en-US",
        enable_automatic_punctuation=True,
        enable_word_confidence=True,
        model="latest_long",
    ):
        prefix = "FINAL" if result["is_final"] else "INTERIM"
        lang_name = result["language_name"]
        print(f"[{lang_name}] {prefix}: {result['transcript']}")

        if result["is_final"] and result["confidence"]:
            print(f"  Confidence: {result['confidence']:.2%}")


if __name__ == "__main__":
    example_usage()
