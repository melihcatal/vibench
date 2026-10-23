from typing import Dict, List, Optional
import assemblyai

ASSEMBLYAI_API_KEY = ""


def get_transcriber(api_key: Optional[str] = None) -> assemblyai.Transcriber:
    key = api_key or ASSEMBLYAI_API_KEY
    config = assemblyai.Settings(api_key=key)
    return assemblyai.Transcriber(config=config)


def transcribe_qa_sample(
    audio_file_path: str,
    api_key: Optional[str] = None,
    language_code: str = "en",
    expected_text: Optional[str] = None,
    word_accuracy_threshold: float = 0.8,
) -> Dict:
    transcriber = get_transcriber(api_key)
    transcript = transcriber.transcribe(
        audio_file_path,
        config=assemblyai.TranscriptionConfig(
            language_code=language_code,
        ),
    )
    result = {
        "transcript_id": transcript.id,
        "status": transcript.status,
        "text": transcript.text,
        "confidence": transcript.confidence,
        "language_code": transcript.language_code,
        "words": transcript.words,
    }
    if expected_text:
        accuracy = _compute_word_accuracy(transcript.text, expected_text)
        result["expected_text"] = expected_text
        result["word_accuracy"] = accuracy
        result["passed_qa"] = accuracy >= word_accuracy_threshold
    return result


def transcribe_qa_batch(
    audio_file_paths: List[str],
    api_key: Optional[str] = None,
    language_code: str = "en",
    expected_texts: Optional[List[str]] = None,
    word_accuracy_threshold: float = 0.8,
) -> List[Dict]:
    results = []
    for i, audio_path in enumerate(audio_file_paths):
        expected = (
            expected_texts[i] if expected_texts and i < len(expected_texts) else None
        )
        result = transcribe_qa_sample(
            audio_file_path=audio_path,
            api_key=api_key,
            language_code=language_code,
            expected_text=expected,
            word_accuracy_threshold=word_accuracy_threshold,
        )
        results.append(result)
    return results


def _compute_word_accuracy(actual: str, expected: str) -> float:
    actual_words = set(actual.lower().split())
    expected_words = set(expected.lower().split())
    if not expected_words:
        return 0.0
    matching = actual_words & expected_words
    return len(matching) / len(expected_words)
