from google.cloud import speech
from typing import Optional, Generator, Tuple


def create_streaming_config(
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    enable_word_confidence: bool = True,
    enable_word_time_offsets: bool = True,
    model: str = "default",
    sample_rate_hertz: int = 16000,
    audio_channel_count: int = 1,
) -> speech.RecognitionConfig:

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_confidence=enable_word_confidence,
        enable_word_time_offsets=enable_word_time_offsets,
        model=model,
        audio_channel_count=audio_channel_count,
    )

    return config


def start_streaming_recognizer(
    audio_generator: Generator[bytes, None, None],
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    client: Optional[speech.SpeechClient] = None,
) -> Generator[Tuple[str, bool], None, None]:

    client = client or speech.SpeechClient()

    config = create_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    def request_generator():
        for audio_content in audio_generator:
            yield speech.StreamingRecognizeRequest(audio_content=audio_content)

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            is_final = result.is_final

            yield transcript, is_final


def create_multi_language_streaming_config(
    primary_language: str = "en-US",
    alternative_languages: Optional[list] = None,
    enable_punctuation: bool = True,
) -> speech.RecognitionConfig:

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=primary_language,
        alternative_language_codes=alternative_languages or [],
        enable_automatic_punctuation=enable_punctuation,
        enable_word_confidence=True,
        model="default",
    )

    return config


def stream_with_language_detection(
    audio_generator: Generator[bytes, None, None],
    possible_languages: list,
    client: Optional[speech.SpeechClient] = None,
) -> Generator[Tuple[str, bool, str], None, None]:

    client = client or speech.SpeechClient()

    config = create_multi_language_streaming_config(
        primary_language=possible_languages[0] if possible_languages else "en-US",
        alternative_languages=possible_languages[1:]
        if len(possible_languages) > 1
        else [],
        enable_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    def request_generator():
        for audio_content in audio_generator:
            yield speech.StreamingRecognizeRequest(audio_content=audio_content)

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            is_final = result.is_final
            detected_language = (
                result.language_code
                if hasattr(result, "language_code")
                else possible_languages[0]
            )

            yield transcript, is_final, detected_language
