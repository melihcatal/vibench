import assemblyai as aai
import os

# Replace with your API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY") 

def diarize_audio(audio_file_path):
    """
    Requests speaker diarization for a recorded meeting using AssemblyAI.

    Args:
        audio_file_path (str): The path to the audio file.

    Returns:
        str: The diarized transcript.
    """
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speaker_diarization=True)

    transcript = transcriber.transcribe(audio_file_path, config)

    if transcript.status == aai.TranscriptStatus.error:
        return f"Error: {transcript.error}"
    else:
        diarized_text = ""
        for utterance in transcript.utterances:
            diarized_text += f"Speaker {utterance.speaker}: {utterance.text}\n"
        return diarized_text

if __name__ == "__main__":
    # Example usage: Replace with your audio file path
    # Make sure to set the ASSEMBLYAI_API_KEY environment variable
    # For example: export ASSEMBLYAI_API_KEY="YOUR_ASSEMBLYAI_API_KEY"
    audio_path = "path/to/your/meeting_audio.mp3"  
    
    if os.path.exists(audio_path):
        print(f"Diarizing audio from: {audio_path}")
        diarized_result = diarize_audio(audio_path)
        print("\n--- Diarized Transcript ---\n")
        print(diarized_result)
    else:
        print(f"Error: Audio file not found at {audio_path}. Please update the 'audio_path' variable.")
