from assemblyai import Client, Transcript
from speech_client import get_assemblyai_client

def get_timestamped_transcript(job_id: str):
    """Returns word or segment timestamps from an AssemblyAI transcription result."""
    client = get_assemblyai_client()
    transcript = client.transcripts.get(job_id)

    if transcript.status == Transcript.Status.completed:
        timestamps = []
        for word_info in transcript.words:
            timestamps.append({
                "word": word_info.text,
                "start": word_info.start,
                "end": word_info.end,
                "speaker": word_info.speaker, # Will be None if diarization is not enabled
            })
        return timestamps
    elif transcript.status == Transcript.Status.error:
        raise Exception(f"AssemblyAI transcription job {job_id} failed: {transcript.error}")
    else:
        return None

if __name__ == '__main__':
    # Example usage: Replace with a real job ID that has completed
    example_job_id = "your_completed_assemblyai_job_id"
    try:
        timestamps = get_timestamped_transcript(example_job_id)
        if timestamps:
            print("Timestamped Transcript:")
            for ts in timestamps[:10]: # Print first 10 words as example
                print(f"  Word: {ts['word']}, Start: {ts['start']}ms, End: {ts['end']}ms, Speaker: {ts['speaker']}")
        else:
            print(f"AssemblyAI job {example_job_id} not yet completed or had an error.")
    except Exception as e:
        print(f"Error getting timestamped transcript: {e}")
