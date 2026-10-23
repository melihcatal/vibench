import os
import time
import assemblyai as aai

def request_diarized_transcript(audio_url: str):
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(
        speaker_labels=True, # Enable speaker diarization
    )

    print(f"Submitting audio from {audio_url} for transcription with diarization...")
    transcript = transcriber.submit(audio_url, config=config)
    job_id = transcript.id

    print(f"Transcription job with diarization submitted with ID: {job_id}")

    while True:
        transcript = transcriber.get_transcript(job_id)
        if transcript.status == aai.TranscriptStatus.completed:
            print("Transcription with diarization completed.")
            if transcript.words:
                diarized_text = []
                current_speaker = None
                for word in transcript.words:
                    if word.speaker != current_speaker:
                        if diarized_text: # Add newline if not the very first word
                            diarized_text.append("\n")
                        diarized_text.append(f"Speaker {word.speaker}: ")
                        current_speaker = word.speaker
                    diarized_text.append(word.text + " ")
                return "".join(diarized_text).strip()
            return transcript.text # Fallback if words are not available for some reason
        elif transcript.status == aai.TranscriptStatus.failed:
            print(f"Transcription failed: {transcript.error}")
            return None
        else:
            print(f"Transcription status: {transcript.status}. Waiting...")
            time.sleep(5) # Wait for 5 seconds before polling again

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # Ensure ASSEMBLYAI_API_KEY is set in your environment
    audio_file_url = "https://storage.googleapis.com/aai-web-samples/5_9_2023_call.wav"
    # diarized_transcript_text = request_diarized_transcript(audio_file_url)
    # if diarized_transcript_text:
    #     print("\nDiarized Transcript:")
    #     print(diarized_transcript_text)
    pass
