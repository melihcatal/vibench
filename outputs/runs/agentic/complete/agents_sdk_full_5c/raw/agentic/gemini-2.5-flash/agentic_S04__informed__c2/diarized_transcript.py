import os
import assemblyai as aai
from speech_models import DiarizationResult

def diarized_transcript(audio_url: str) -> str:
    """Requests speaker diarization for a recorded meeting using AssemblyAI."""
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    config = aai.TranscriptionConfig(
        speaker_labels=True,
        punctuate=True,
        format_text=True
    )
    
    transcriber = aai.Transcriber()
    transcript = transcriber.submit_for_transcription(audio_url, config)
    
    return transcript.id


def get_diarized_transcript_result(job_id: str) -> DiarizationResult or None:
    """Retrieves the diarized transcript result from AssemblyAI."""
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript_by_id(job_id)

    if transcript.status == aai.TranscriptStatus.completed:
        speakers = []
        for utterance in transcript.utterances:
            speakers.append({"speaker": utterance.speaker, "text": utterance.text})
        return DiarizationResult(speakers=speakers, status=transcript.status.value)
    elif transcript.status == aai.TranscriptStatus.failed:
        raise Exception(f"Diarization job {job_id} failed: {transcript.error}")
    
    return DiarizationResult(speakers=None, status=transcript.status.value)

if __name__ == "__main__":
    # Example usage (replace with actual audio URL and job ID)
    # audio_file_url = "https://example.com/meeting.mp3"
    # job_id = diarized_transcript(audio_file_url)
    # print(f"Submitted diarization job with ID: {job_id}")
    # 
    # # In a real scenario, you'd poll the job_id until it's completed
    # # result = get_diarized_transcript_result(job_id)
    # # if result and result.speakers:
    # #     for speaker_utterance in result.speakers:
    # #         print(f"Speaker {speaker_utterance['speaker']}: {speaker_utterance['text']}")
    pass
