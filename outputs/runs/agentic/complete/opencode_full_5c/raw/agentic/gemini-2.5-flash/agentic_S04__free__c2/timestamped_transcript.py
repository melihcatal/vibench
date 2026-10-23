from poll_transcription import poll_transcription
from speech_models import WordInfo, TranscriptionJob
from typing import List, Optional


def get_timestamped_transcript(operation_name: str) -> Optional[List[WordInfo]]:
    job = poll_transcription(operation_name)

    if job.status == "COMPLETED" and job.results:
        all_word_info = []
        for alternative in job.results.alternatives:
            all_word_info.extend(alternative.words)
        return all_word_info
    return None
