from typing import List, Dict
from speech_models import TranscriptionResult

def get_diarized_transcript(transcription_result: TranscriptionResult) -> List[Dict]:
    diarized_segments = []
    if transcription_result and transcription_result.recognized_phrases:
        for phrase in transcription_result.recognized_phrases:
            speaker_id = phrase.get('speaker') # Azure Speech output includes 'speaker' property if diarization is enabled
            text = phrase.get('display')
            offset_ms = phrase.get('offsetInTicks', 0) / 10000 # Convert ticks to milliseconds
            duration_ms = phrase.get('durationInTicks', 0) / 10000 # Convert ticks to milliseconds
            if speaker_id is not None and text:
                diarized_segments.append({
                    "speaker_id": speaker_id,
                    "text": text,
                    "offset_ms": offset_ms,
                    "duration_ms": duration_ms
                })
    return diarized_segments
