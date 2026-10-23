import os
import time
import assemblyai as aai
from typing import List, Dict, Any

def get_timestamped_transcript(job_id: str) -> List[Dict[str, Any]] | None:
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()

    print(f"Fetching timestamped transcript for job ID: {job_id}")
    while True:
        transcript = transcriber.get_transcript(job_id)
        if transcript.status == aai.TranscriptStatus.completed:
            print("Transcription completed. Extracting timestamps.")
            if transcript.words:
                timestamped_words = [
                    {
                        "word": word.text,
                        "start": word.start,
                        "end": word.end,
                        "speaker": word.speaker
                    }
                    for word in transcript.words
                ]
                return timestamped_words
            else:
                print("No words found in the transcript for timestamps.")
                return None
        elif transcript.status == aai.TranscriptStatus.failed:
            print(f"Transcription failed: {transcript.error}")
            return None
        else:
            print(f"Transcription status: {transcript.status}. Waiting...")
            time.sleep(5) # Wait for 5 seconds before polling again

if __name__ == "__main__":
    # Example usage (replace with actual job ID of a completed transcript)
    # Ensure ASSEMBLYAI_API_KEY is set in your environment
    # job_id = "YOUR_COMPLETED_TRANSCRIPTION_JOB_ID"
    # timestamps = get_timestamped_transcript(job_id)
    # if timestamps:
    #     print("\nTimestamped Transcript Words:")
    #     for word_info in timestamps[:10]: # Print first 10 words
    #         print(f"  Word: '{word_info['word']}', Start: {word_info['start']}ms, End: {word_info['end']}ms, Speaker: {word_info['speaker']}")
    pass
