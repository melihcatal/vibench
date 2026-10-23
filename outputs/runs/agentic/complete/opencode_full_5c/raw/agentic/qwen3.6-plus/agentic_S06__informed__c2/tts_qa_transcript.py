import os
import time
import assemblyai as aai
from typing import Optional


ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


def get_assemblyai_config() -> aai.Configuration:
    api_key = os.environ.get(ASSEMBLYAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"AssemblyAI API key not found. Set the {ASSEMBLYAI_API_KEY_ENV} environment variable."
        )
    return aai.Configuration(api_key=api_key)


def transcribe_qa_audio(
    audio_file_path: str,
    language_code: str = "en",
    speaker_labels: bool = False,
) -> dict:
    config = get_assemblyai_config()
    aai.settings.configure(config)

    transcriber = aai.Transcriber()

    config_obj = aai.TranscriptionConfig(
        language_code=language_code,
        speaker_labels=speaker_labels,
    )

    transcript = transcriber.transcribe(audio_file_path, config=config_obj)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"AssemblyAI transcription failed: {transcript.error}")

    return {
        "text": transcript.text,
        "words": [
            {
                "text": w.text,
                "start": w.start,
                "end": w.end,
                "confidence": w.confidence,
            }
            for w in transcript.words
        ]
        if transcript.words
        else [],
        "utterances": [
            {
                "speaker": u.speaker,
                "text": u.text,
            }
            for u in transcript.utterances
        ]
        if transcript.utterances
        else [],
        "provider": "assemblyai",
        "language_code": language_code,
    }


def transcribe_qa_audio_bytes(
    audio_bytes: bytes,
    language_code: str = "en",
    speaker_labels: bool = False,
) -> dict:
    config = get_assemblyai_config()
    aai.settings.configure(config)

    transcriber = aai.Transcriber()

    config_obj = aai.TranscriptionConfig(
        language_code=language_code,
        speaker_labels=speaker_labels,
    )

    transcript = transcriber.transcribe(audio_bytes, config=config_obj)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"AssemblyAI transcription failed: {transcript.error}")

    return {
        "text": transcript.text,
        "words": [
            {
                "text": w.text,
                "start": w.start,
                "end": w.end,
                "confidence": w.confidence,
            }
            for w in transcript.words
        ]
        if transcript.words
        else [],
        "provider": "assemblyai",
        "language_code": language_code,
    }


def verify_tts_output(
    original_text: str,
    audio_file_path: str,
    similarity_threshold: float = 0.7,
    language_code: str = "en",
) -> dict:
    transcript_result = transcribe_qa_audio(
        audio_file_path, language_code=language_code
    )
    transcribed_text = transcript_result["text"]

    original_normalized = " ".join(original_text.lower().split())
    transcribed_normalized = " ".join(transcribed_text.lower().split())

    original_words = set(original_normalized.split())
    transcribed_words = set(transcribed_normalized.split())

    if len(original_words) == 0:
        word_overlap = 1.0
    else:
        word_overlap = len(original_words & transcribed_words) / len(original_words)

    passed = word_overlap >= similarity_threshold

    return {
        "passed": passed,
        "word_overlap": word_overlap,
        "similarity_threshold": similarity_threshold,
        "original_text": original_text,
        "transcribed_text": transcribed_text,
        "provider": "assemblyai",
    }
