import os
import assemblyai as aai
from speech_client import get_assemblyai_client


def diarized_transcript(audio_url):
    """Request speaker diarization for a recorded meeting using AssemblyAI."""
    client = get_assemblyai_client()

    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=2,
        language_code="en",
        punctuate=True,
        format_text=True,
    )

    transcript = client.transcribe.submit(audio_url=audio_url, config=config)

    # Wait for completion
    while transcript.status not in [
        aai.TranscriptStatus.completed,
        aai.TranscriptStatus.error,
    ]:
        transcript = client.transcript.get(transcript.id)
        if transcript.status == aai.TranscriptStatus.completed:
            break

    if transcript.status == aai.TranscriptStatus.completed:
        utterances = transcript.utterances if transcript.utterances else []

        diarized_result = []
        for utterance in utterances:
            diarized_result.append(
                {
                    "speaker": utterance.speaker,
                    "text": utterance.text,
                    "start": utterance.start,
                    "end": utterance.end,
                    "confidence": utterance.confidence,
                }
            )

        return {
            "job_id": transcript.id,
            "status": "completed",
            "diarized_segments": diarized_result,
            "speaker_count": len(set([utt.speaker for utt in utterances]))
            if utterances
            else 0,
            "provider": "AssemblyAI",
        }
    else:
        return {
            "job_id": transcript.id,
            "status": "error",
            "error": transcript.error,
            "provider": "AssemblyAI",
        }
