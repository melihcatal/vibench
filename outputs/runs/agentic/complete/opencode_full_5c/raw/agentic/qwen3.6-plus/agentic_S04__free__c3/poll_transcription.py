from typing import Dict, Any

from speech_client import create_assemblyai_session, poll_until_complete
from speech_models import TranscriptionResult


def poll_transcription(
    transcript_id: str, poll_interval: float = 3.0, max_attempts: int = 200
) -> Dict[str, Any]:
    session = create_assemblyai_session()

    result_data = poll_until_complete(
        session,
        transcript_id,
        poll_interval=poll_interval,
        max_attempts=max_attempts,
    )

    transcription = TranscriptionResult.from_assemblyai_response(result_data)

    return {
        "transcript_id": transcription.transcript_id,
        "status": transcription.status,
        "text": transcription.text,
        "confidence": transcription.confidence,
        "audio_duration": transcription.audio_duration,
        "word_count": len(transcription.words),
        "utterance_count": len(transcription.utterances),
        "words": [
            {
                "text": w.text,
                "start": w.start,
                "end": w.end,
                "confidence": w.confidence,
            }
            for w in transcription.words
        ],
    }


def get_transcript_text(transcript_id: str) -> str:
    result = poll_transcription(transcript_id)
    return result["text"]


if __name__ == "__main__":
    import sys

    tid = sys.argv[1] if len(sys.argv) > 1 else None
    if not tid:
        print("Usage: python poll_transcription.py <transcript_id>")
        sys.exit(1)

    result = poll_transcription(tid)
    print(result)
