import os
import time
import assemblyai as aai

def get_diarized_transcript(audio_url: str) -> list[dict]:
    """
    Requests speaker diarization for a recorded meeting and returns the diarized transcript.

    Args:
        audio_url: The URL of the audio file to transcribe.

    Returns:
        A list of dictionaries, where each dictionary represents a speaker segment
        with 'speaker' and 'text' keys. Returns an empty list if transcription fails.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    
    # Configure for diarization
    config = aai.TranscriptionConfig(speaker_labels=True, language_code="en_us")
    
    print(f"Submitting audio for diarization: {audio_url}")
    transcript = transcriber.submit(audio_url, config=config)
    
    while True:
        transcript = transcriber.get_transcript_by_id(transcript.id)
        
        if transcript.status == aai.TranscriptStatus.completed:
            if transcript.utterances:
                diarized_output = []
                for utterance in transcript.utterances:
                    diarized_output.append({
                        "speaker": utterance.speaker,
                        "text": utterance.text
                    })
                return diarized_output
            else:
                print("Diarization completed but no utterances found.")
                return []
        elif transcript.status == aai.TranscriptStatus.failed:
            print(f"Diarization job {transcript.id} failed.")
            return []
        else:
            print(f"Diarization job {transcript.id} is {transcript.status}. Waiting...")
            time.sleep(5)

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # diarized_segments = get_diarized_transcript("https://example.com/meeting_audio.mp3")
    # if diarized_segments:
    #     for segment in diarized_segments:
    #         print(f"{segment['speaker']}: {segment['text']}")
    pass