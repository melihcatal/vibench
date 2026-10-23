import os
import assemblyai as aai


def transcribe_qa_sample(audio_file_path: str) -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)
    return transcript.text


def transcribe_qa_sample_with_config(
    audio_file_path: str, language_code: str = "en", speaker_labels: bool = False
) -> dict:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(
        language_code=language_code,
        speaker_labels=speaker_labels,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path, config=config)
    result = {
        "text": transcript.text,
        "confidence": transcript.confidence,
        "words": [
            {"text": w.text, "start": w.start, "end": w.end, "confidence": w.confidence}
            for w in (transcript.words or [])
        ],
    }
    if speaker_labels and transcript.utterances:
        result["utterances"] = [
            {"speaker": u.speaker, "text": u.text, "start": u.start, "end": u.end}
            for u in transcript.utterances
        ]
    return result


def verify_transcript_matches_expected(
    audio_file_path: str, expected_text: str, threshold: float = 0.8
) -> dict:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)
    transcribed_text = transcript.text.lower().strip()
    expected_lower = expected_text.lower().strip()
    trans_words = set(transcribed_text.split())
    expected_words = set(expected_lower.split())
    if not expected_words:
        match_score = 1.0 if not trans_words else 0.0
    else:
        overlap = trans_words & expected_words
        match_score = len(overlap) / len(expected_words)
    return {
        "transcribed_text": transcribed_text,
        "expected_text": expected_lower,
        "match_score": match_score,
        "passed": match_score >= threshold,
        "confidence": transcript.confidence,
    }
