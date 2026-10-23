import os
from typing import Iterator, List, Optional
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIClientError


def start_streaming_recognizer(
    audio_stream: Iterator[bytes],
    language_code: str = "en-US",
    alternative_language_codes: Optional[List[str]] = None,
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    max_alternatives: int = 1,
    sample_rate_hertz: int = 16000,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_spoken_punctuation: bool = True,
    diarization_config: Optional[dict] = None,
) -> Iterator[dict]:
    client = speech.SpeechClient()

    config_kwargs = {
        "encoding": encoding,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "model": model,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "enable_word_time_offsets": enable_word_time_offsets,
        "profanity_filter": profanity_filter,
        "max_alternatives": max_alternatives,
    }

    if alternative_language_codes:
        config_kwargs["alternative_language_codes"] = alternative_language_codes

    if enable_spoken_punctuation:
        config_kwargs["enable_spoken_punctuation"] = True

    if diarization_config:
        config_kwargs["diarization_config"] = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=diarization_config.get("enable", True),
            min_speaker_count=diarization_config.get("min_speakers", 2),
            max_speaker_count=diarization_config.get("max_speakers", 6),
        )

    recognition_config = speech.RecognitionConfig(**config_kwargs)

    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )

    def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        for audio_chunk in audio_stream:
            yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=request_generator(),
    )

    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue

            best_alt = result.alternatives[0]
            speaker_tag = None
            if diarization_config and best_alt.words:
                speaker_tags = set()
                for word in best_alt.words:
                    if hasattr(word, "speaker_tag"):
                        speaker_tags.add(word.speaker_tag)
                if speaker_tags:
                    speaker_tag = list(speaker_tags)[0]

            yield {
                "transcript": best_alt.transcript,
                "is_final": result.is_final,
                "confidence": best_alt.confidence,
                "stability": result.stability,
                "language_code": language_code,
                "result_end_time": result.result_end_time.total_seconds()
                if result.result_end_time
                else 0.0,
                "result_start_time": result.result_start_time.total_seconds()
                if result.result_start_time
                else 0.0,
                "speaker_tag": speaker_tag,
                "words": [
                    {
                        "word": w.word,
                        "start_time": w.start_time.total_seconds()
                        if w.start_time
                        else 0.0,
                        "end_time": w.end_time.total_seconds() if w.end_time else 0.0,
                        "confidence": w.confidence,
                        "speaker_tag": getattr(w, "speaker_tag", None),
                    }
                    for w in best_alt.words
                ]
                if enable_word_time_offsets
                else [],
            }


def create_recognizer_with_settings(
    language_code: str = "en-US",
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    max_alternatives: int = 1,
    sample_rate_hertz: int = 16000,
    alternative_language_codes: Optional[List[str]] = None,
) -> speech.StreamingRecognitionConfig:
    config_kwargs = {
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "model": model,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "enable_word_time_offsets": enable_word_time_offsets,
        "profanity_filter": profanity_filter,
        "max_alternatives": max_alternatives,
    }

    if alternative_language_codes:
        config_kwargs["alternative_language_codes"] = alternative_language_codes

    recognition_config = speech.RecognitionConfig(**config_kwargs)

    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )
