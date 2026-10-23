import os
import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionConfig, TranscriptionJob

def get_timestamped_transcript(audio_url: str) -> TranscriptionJob:
    """
    Submits an audio file for transcription and returns word-level timestamps.
    This function combines submission and polling for simplicity.
    """
    client = get_assemblyai_client()
    
    transcriber = aai.Transcriber()
    
    # Submit with word_timestamps enabled (AssemblyAI enables this by default and provides 'words' list)
    # No specific config needed for basic word timestamps as it's included in the Word object.
    # To ensure word-level data is returned, we can simply rely on the default behavior
    # of the SDK providing the `words` attribute in the Transcript object.
    config = aai.TranscriptionConfig(word_timestamps=True) # Explicitly request word timestamps
    transcript_object = transcriber.transcribe(audio_url, config=config) # This blocks until complete
    
    if transcript_object.status == aai.TranscriptStatus.completed:
        words_data = []
        if transcript_object.words:
            for word_obj in transcript_object.words:
                words_data.append({
                    "text": word_obj.text,
                    "start": word_obj.start, # Milliseconds
                    "end": word_obj.end,     # Milliseconds
                    "confidence": word_obj.confidence
                })
        
        return TranscriptionJob(
            id=transcript_object.id,
            status=transcript_object.status,
            transcript=transcript_object.text,
            words=words_data
        )
    else:
        return TranscriptionJob(
            id=transcript_object.id,
            status=transcript_object.status,
            transcript=None,
            words=None
        )

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    audio_url = "https://example.com/sample_speech.mp3" # Use a public audio URL
    
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    else:
        print(f"Requesting timestamped transcript for: {audio_url}")
        result = get_timestamped_transcript(audio_url)
        print(f"Job ID: {result.id}")
        print(f"Status: {result.status}")
        if result.status == aai.TranscriptStatus.completed and result.words:
            print("\n--- Word-level Timestamps ---")
            for word in result.words[:10]: # Print first 10 words
                print(f"'{word['text']}' - Start: {word['start'] / 1000:.2f}s, End: {word['end'] / 1000:.2f}s, Confidence: {word['confidence']:.2f}")
            if len(result.words) > 10:
                print("...")
        elif result.status != aai.TranscriptStatus.completed:
            print("Transcription not completed yet.")
