import os
import time
import assemblyai as aai

def get_timestamped_transcript(audio_url: str, output_type: str = "words") -> list[dict]:
    """
    Requests a transcription with word or segment timestamps from AssemblyAI.

    Args:
        audio_url: The URL of the audio file to transcribe.
        output_type: 'words' for word-level timestamps or 'segments' for segment-level.

    Returns:
        A list of dictionaries, where each dictionary contains text and start/end timestamps.
        Returns an empty list if transcription fails.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    
    # Configure for word-level timestamps (segments are available by default in utterances)
    config = aai.TranscriptionConfig(word_timestamps=True, language_code="en_us")
    
    print(f"Submitting audio for timestamped transcription: {audio_url}")
    transcript = transcriber.submit(audio_url, config=config)
    
    while True:
        transcript = transcriber.get_transcript_by_id(transcript.id)
        
        if transcript.status == aai.TranscriptStatus.completed:
            timestamped_output = []
            if output_type == "words" and transcript.words:
                for word_info in transcript.words:
                    timestamped_output.append({
                        "text": word_info.text,
                        "start": word_info.start,
                        "end": word_info.end
                    })
            elif output_type == "segments" and transcript.utterances:
                for utterance in transcript.utterances:
                    timestamped_output.append({
                        "text": utterance.text,
                        "start": utterance.start,
                        "end": utterance.end
                    })
            elif output_type == "segments" and transcript.segments: # Fallback for non-diarized segments
                 for segment in transcript.segments:
                    timestamped_output.append({
                        "text": segment.text,
                        "start": segment.start,
                        "end": segment.end
                    })
            return timestamped_output
        elif transcript.status == aai.TranscriptStatus.failed:
            print(f"Timestamped transcription job {transcript.id} failed.")
            return []
        else:
            print(f"Timestamped transcription job {transcript.id} is {transcript.status}. Waiting...")
            time.sleep(5)

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # word_timestamps = get_timestamped_transcript("https://example.com/audio.mp3", output_type="words")
    # if word_timestamps:
    #     for word in word_timestamps:
    #         print(f"'{word['text']}' - Start: {word['start']}ms, End: {word['end']}ms")

    # segment_timestamps = get_timestamped_transcript("https://example.com/audio.mp3", output_type="segments")
    # if segment_timestamps:
    #     for segment in segment_timestamps:
    #         print(f"'{segment['text']}' - Start: {segment['start']}ms, End: {segment['end']}ms")
    pass