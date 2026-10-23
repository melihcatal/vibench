import assemblyai
from speech_client import assemblyai_client
from speech_models import DiarizedSegment, TranscriptionResult

def get_diarized_transcript(audio_url: str) -> TranscriptionResult:
    """
    Submits an audio file for transcription with speaker diarization enabled
    and returns the diarized segments. This is a simplified example
    that assumes the job completes quickly for demonstration.

    Args:
        audio_url: The publicly accessible URL of the audio file.

    Returns:
        A TranscriptionResult object containing the diarized segments.
    """
    config = assemblyai.TranscriptionConfig(speaker_labels=True)
    
    # In a real application, you would submit and poll separately.
    # For simplicity, this example uses the blocking transcribe method.
    transcript = assemblyai_client.transcribe(audio_url, config)

    if transcript.status == 'error':
        raise Exception(f"Diarization job failed with error: {transcript.error}")

    segments = []
    if transcript.utterances:
        for utterance in transcript.utterances:
            segments.append(
                DiarizedSegment(
                    speaker=utterance.speaker,
                    text=utterance.text,
                    start=utterance.start,
                    end=utterance.end,
                )
            )
            
    return TranscriptionResult(
        job_id=transcript.id,
        transcript_text=transcript.text or "",
        diarized_segments=segments
    )
