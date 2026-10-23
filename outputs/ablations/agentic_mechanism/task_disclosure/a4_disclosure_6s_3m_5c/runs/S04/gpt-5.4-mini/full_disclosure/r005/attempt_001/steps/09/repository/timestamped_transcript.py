import os
from typing import Any, Dict, List, Literal, Optional, Union

from google.cloud import speech_v1 as speech


TimestampMode = Literal["word", "segment"]


def _client() -> speech.SpeechClient:
    return speech.SpeechClient()


def _load_audio(uri: Optional[str] = None, content: Optional[bytes] = None) -> speech.RecognitionAudio:
    if uri:
        return speech.RecognitionAudio(uri=uri)
    if content is not None:
        return speech.RecognitionAudio(content=content)
    raise ValueError("Either uri or content must be provided")


def _word_entries(result: Any) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for word_info in getattr(result, "words", []) or []:
        start = getattr(word_info.start_time, "total_seconds", lambda: None)()
        end = getattr(word_info.end_time, "total_seconds", lambda: None)()
        entries.append({"word": word_info.word, "start_time": start, "end_time": end})
    return entries


def _segment_entries(result: Any) -> List[Dict[str, Any]]:
    segments: List[Dict[str, Any]] = []
    alternatives = getattr(result, "alternatives", []) or []
    if not alternatives:
        return segments
    alt = alternatives[0]
    words = list(getattr(alt, "words", []) or [])
    if not words:
        return segments
    current_speaker = getattr(words[0], "speaker_tag", None)
    current_words = []
    segment_start = getattr(words[0].start_time, "total_seconds", lambda: None)()
    for word_info in words:
        speaker = getattr(word_info, "speaker_tag", None)
        if speaker != current_speaker and current_words:
            last_word = current_words[-1]
            segments.append({
                "speaker": current_speaker,
                "start_time": segment_start,
                "end_time": getattr(last_word.end_time, "total_seconds", lambda: None)(),
                "text": " ".join(w.word for w in current_words),
            })
            current_words = []
            segment_start = getattr(word_info.start_time, "total_seconds", lambda: None)()
            current_speaker = speaker
        current_words.append(word_info)
    if current_words:
        last_word = current_words[-1]
        segments.append({
            "speaker": current_speaker,
            "start_time": segment_start,
            "end_time": getattr(last_word.end_time, "total_seconds", lambda: None)(),
            "text": " ".join(w.word for w in current_words),
        })
    return segments


def timestamped_transcript(
    audio_uri: Optional[str] = None,
    audio_content: Optional[bytes] = None,
    mode: TimestampMode = "segment",
    language_code: str = "en-US",
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    client = _client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
        enable_word_time_offsets=True,
        enable_speaker_diarization=(mode == "segment"),
        diarization_speaker_count=2 if mode == "segment" else 0,
    )
    audio = _load_audio(uri=audio_uri, content=audio_content)
    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return [] if mode == "word" else {"segments": []}
    result = response.results[-1]
    if mode == "word":
        return _word_entries(result)
    return {"segments": _segment_entries(result)}


def main() -> None:
    audio_uri = os.getenv("GCS_AUDIO_URI")
    mode = os.getenv("TIMESTAMP_MODE", "segment")
    output = timestamped_transcript(audio_uri=audio_uri, mode=mode)  # type: ignore[arg-type]
    print(output)


if __name__ == "__main__":
    main()
