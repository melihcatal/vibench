from google.cloud import speech_v1p1beta1 as speech
from typing import Optional, List, Dict, Any


class LanguageAwareStreamingRecognizer:
    def __init__(self, project_id: Optional[str] = None):
        self.client = speech.SpeechClient()
        self.project_id = project_id

    def create_streaming_config(
        self,
        language_code: str = "en-US",
        enable_automatic_punctuation: bool = True,
        enable_word_time_offsets: bool = False,
        enable_word_confidence: bool = True,
        model: str = "latest_long",
        use_enhanced: bool = True,
        alternative_language_codes: Optional[List[str]] = None,
        speech_contexts: Optional[List[Dict[str, Any]]] = None,
    ) -> speech.StreamingRecognitionConfig:

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
            enable_word_time_offsets=enable_word_time_offsets,
            enable_word_confidence=enable_word_confidence,
            model=model,
            use_enhanced=use_enhanced,
        )

        if alternative_language_codes:
            config.alternative_language_codes = alternative_language_codes

        if speech_contexts:
            config.speech_contexts = [
                speech.SpeechContext(phrases=ctx.get("phrases", []))
                for ctx in speech_contexts
            ]

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
            single_utterance=False,
        )

        return streaming_config

    def start_streaming_recognition(
        self,
        audio_generator,
        language_code: str = "en-US",
        punctuation: bool = True,
        **kwargs,
    ):
        streaming_config = self.create_streaming_config(
            language_code=language_code,
            enable_automatic_punctuation=punctuation,
            **kwargs,
        )

        def request_generator():
            for chunk in audio_generator:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

        requests = request_generator()

        responses = self.client.streaming_recognize(
            config=streaming_config,
            requests=requests,
        )

        return responses

    def stream_with_multiple_languages(
        self,
        audio_generator,
        primary_language: str = "en-US",
        secondary_languages: Optional[List[str]] = None,
        **kwargs,
    ):
        if secondary_languages is None:
            secondary_languages = []

        return self.start_streaming_recognition(
            audio_generator,
            language_code=primary_language,
            alternative_language_codes=secondary_languages,
            **kwargs,
        )

    def create_speech_context(
        self, phrases: List[str], boost: float = 20.0
    ) -> Dict[str, Any]:
        return {"phrases": phrases, "boost": boost}

    def get_supported_languages(self) -> List[str]:
        return [
            "en-US",
            "en-GB",
            "es-ES",
            "fr-FR",
            "de-DE",
            "it-IT",
            "ja-JP",
            "ko-KR",
            "pt-BR",
            "ru-RU",
            "zh-CN",
            "zh-TW",
        ]

    def validate_language_code(self, language_code: str) -> bool:
        supported = self.get_supported_languages()
        return language_code in supported
