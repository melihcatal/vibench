import os
import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionConfig, TranscriptionJob

def get_diarized_transcript(audio_url: str) -> TranscriptionJob:
    """
    Submits an audio file for transcription with speaker diarization enabled
    and returns the diarized transcript. This function combines submission and polling
    for simplicity, but in a real batch scenario, you'd poll separately.
    """
    client = get_assemblyai_client()
    
    transcriber = aai.Transcriber()
    
    # Submit with speaker_labels enabled
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript_object = transcriber.transcribe(audio_url, config=config) # This blocks until complete
    
    if transcript_object.status == aai.TranscriptStatus.completed:
        # Extract utterances which contain speaker information
        utterances_data = []
        if transcript_object.utterances:
            for utterance in transcript_object.utterances:
                utterances_data.append({
                    "speaker": utterance.speaker,
                    "text": utterance.text,
                    "start": utterance.start,
                    "end": utterance.end,
                })
        
        return TranscriptionJob(
            id=transcript_object.id,
            status=transcript_object.status,
            transcript=transcript_object.text,
            utterances=utterances_data
        )
    else:
        return TranscriptionJob(
            id=transcript_object.id,
            status=transcript_object.status,
            transcript=None,
            utterances=None
        )

if __name__ == "__main__":
    # Example usage (replace with actual audio URL for a meeting)
    audio_url = "https://example.com/meeting_audio.mp3" # Use a public audio URL with multiple speakers
    
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    else:
        print(f"Requesting diarized transcript for: {audio_url}")
        result = get_diarized_transcript(audio_url)
        print(f"Job ID: {result.id}")
        print(f"Status: {result.status}")
        if result.status == aai.TranscriptStatus.completed and result.utterances:
            print("\n--- Diarized Transcript ---")
            for utterance in result.utterances:
                print(f"Speaker {utterance['speaker']}: {utterance['text']} ({utterance['start'] / 1000:.2f}s - {utterance['end'] / 1000:.2f}s)")
        elif result.status != aai.TranscriptStatus.completed:
            print("Transcription not completed yet.")
