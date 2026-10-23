import os
import assemblyai as aai
from typing import Optional, Dict, Any
import tempfile


def transcribe_audio_file(filepath: str) -> Dict[str, Any]:
    """
    Transcribe synthesized QA samples to verify spoken output using AssemblyAI.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key

    try:
        transcriber = aai.Transcriber()

        config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)

        transcript = transcriber.transcribe(filepath, config=config)

        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")

        return {
            "text": transcript.text,
            "words": [
                {"text": word.text, "start": word.start, "end": word.end}
                for word in transcript.words
            ],
            "confidence": transcript.confidence,
            "language": transcript.language_code,
            "speakers": transcript.utterances
            if hasattr(transcript, "utterances")
            else [],
        }

    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")


def transcribe_audio_bytes(
    audio_bytes: bytes, audio_format: str = "mp3"
) -> Dict[str, Any]:
    """
    Transcribe audio bytes to verify spoken output.
    """
    with tempfile.NamedTemporaryFile(
        suffix=f".{audio_format}", delete=False
    ) as temp_file:
        temp_file.write(audio_bytes)
        temp_file.flush()

        try:
            result = transcribe_audio_file(temp_file.name)
            os.unlink(temp_file.name)
            return result
        except Exception as e:
            os.unlink(temp_file.name)
            raise e


def verify_tts_output(
    original_text: str,
    audio_bytes: bytes,
    audio_format: str = "mp3",
    similarity_threshold: float = 0.8,
) -> Dict[str, Any]:
    """
    Verify TTS output by comparing original text with transcription.
    """
    try:
        transcription = transcribe_audio_bytes(audio_bytes, audio_format)
        transcribed_text = transcription["text"]

        from difflib import SequenceMatcher

        similarity = SequenceMatcher(
            None, original_text.lower(), transcribed_text.lower()
        ).ratio()

        words_original = set(original_text.lower().split())
        words_transcribed = set(transcribed_text.lower().split())
        common_words = words_original.intersection(words_transcribed)
        word_coverage = len(common_words) / len(words_original) if words_original else 0

        is_accurate = similarity >= similarity_threshold

        return {
            "is_accurate": is_accurate,
            "similarity_score": similarity,
            "word_coverage": word_coverage,
            "original_text": original_text,
            "transcribed_text": transcribed_text,
            "transcription_details": transcription,
        }

    except Exception as e:
        raise Exception(f"TTS verification failed: {str(e)}")
