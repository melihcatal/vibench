from google.cloud import speech_v1p1beta1 as speech
from typing import Generator, Dict, Any


def start_streaming_recognizer(
    audio_generator: Generator[bytes, None, None],
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    enable_word_confidence: bool = True,
    enable_word_time_offsets: bool = True,
    model: str = "default",
    use_enhanced: bool = False,
) -> Generator[Dict[str, Any], None, None]:

    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        enable_word_confidence=enable_word_confidence,
        enable_word_time_offsets=enable_word_time_offsets,
        model=model,
        use_enhanced=use_enhanced,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=False,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator
    )

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence

            word_info = []
            if (
                hasattr(result.alternatives[0], "words")
                and result.alternatives[0].words
            ):
                for word in result.alternatives[0].words:
                    word_info.append(
                        {
                            "word": word.word,
                            "confidence": word.confidence,
                            "start_time": word.start_time.total_seconds()
                            if word.start_time
                            else None,
                            "end_time": word.end_time.total_seconds()
                            if word.end_time
                            else None,
                        }
                    )

            yield {
                "transcript": transcript,
                "is_final": result.is_final,
                "confidence": confidence,
                "language_code": language_code,
                "model": model,
                "use_enhanced": use_enhanced,
                "words": word_info,
                "stability": getattr(result, "stability", None),
                "result_end_time": result.result_end_time.total_seconds()
                if result.result_end_time
                else None,
            }


def create_language_specific_streamer(language_code, **kwargs):
    def streamer(audio_generator):
        return start_streaming_recognizer(
            audio_generator, language_code=language_code, **kwargs
        )

    return streamer


ENGLISH_STREAMER = create_language_specific_streamer("en-US", enable_punctuation=True)
SPANISH_STREAMER = create_language_specific_streamer("es-ES", enable_punctuation=True)
FRENCH_STREAMER = create_language_specific_streamer("fr-FR", enable_punctuation=True)
GERMAN_STREAMER = create_language_specific_streamer("de-DE", enable_punctuation=True)
JAPANESE_STREAMER = create_language_specific_streamer("ja-JP", enable_punctuation=False)
CHINESE_STREAMER = create_language_specific_streamer("zh-CN", enable_punctuation=False)
