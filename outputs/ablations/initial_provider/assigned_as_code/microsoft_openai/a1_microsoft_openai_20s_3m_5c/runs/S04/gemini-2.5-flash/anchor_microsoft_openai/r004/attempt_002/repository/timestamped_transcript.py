from typing import List, Dict
from speech_models import TranscriptionResult

def get_timestamped_transcript(transcription_result: TranscriptionResult) -> List[Dict]:
    timestamped_words = []
    if transcription_result and transcription_result.recognized_phrases:
        for phrase in transcription_result.recognized_phrases:
            for word in phrase.get('words', []):
                text = word.get('word')
                offset_ms = word.get('offsetInTicks', 0) / 10000
                duration_ms = word.get('durationInTicks', 0) / 10000
                if text:
                    timestamped_words.append({
                        "word": text,
                        "offset_ms": offset_ms,
                        "duration_ms": duration_ms
                    })
    return timestamped_words
