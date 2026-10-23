import assemblyai as aai
import os
import time

# Replace with your AssemblyAI API key
# You can set it as an environment variable or directly here
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY", "YOUR_ASSEMBLYAI_API_KEY")

def poll_transcription_job(transcript_id):
    """
    Polls a transcription job from AssemblyAI and returns the transcript.
    """
    if not aai.settings.api_key or aai.settings.api_key == "YOUR_ASSEMBLYAI_API_KEY":
        raise ValueError("AssemblyAI API key not set. Please set the ASSEMBLYAI_API_KEY environment variable or replace 'YOUR_ASSEMBLYAI_API_KEY'.")

    while True:
        try:
            transcript = aai.Transcript.get_by_id(transcript_id)
            if transcript.status == aai.TranscriptStatus.completed:
                return transcript.text
            elif transcript.status == aai.TranscriptStatus.failed:
                raise Exception(f"Transcription failed: {transcript.error}")
            elif transcript.status == aai.TranscriptStatus.queued or transcript.status == aai.TranscriptStatus.processing:
                print(f"Transcription job {transcript_id} is {transcript.status}. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before polling again
            else:
                raise Exception(f"Unknown transcription status: {transcript.status}")
        except aai.exceptions.APIError as e:
            raise Exception(f"AssemblyAI API error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage (replace with a real transcript ID)
    # You would typically get this transcript_id after submitting an audio file for transcription
    example_transcript_id = "YOUR_TRANSCRIPT_ID_HERE"
    
    if example_transcript_id == "YOUR_TRANSCRIPT_ID_HERE":
        print("Please replace 'YOUR_TRANSCRIPT_ID_HERE' with a real AssemblyAI transcript ID for testing.")
    else:
        try:
            transcript_text = poll_transcription_job(example_transcript_id)
            print("Transcription completed successfully:")
            print(transcript_text)
        except Exception as e:
            print(f"Error polling transcription: {e}")
