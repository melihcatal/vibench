import assemblyai as aai
import os

def get_timestamped_transcript(audio_file_path):
    """
    Transcribes an audio file and returns word or segment timestamps.

    Args:
        audio_file_path (str): The path to the audio file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a word
              and contains 'text', 'start' (timestamp in ms), and 'end' (timestamp in ms).
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(word_boost=["AssemblyAI"], boost_param="high")
    transcript = transcriber.transcribe(audio_file_path, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    word_timestamps = []
    if transcript.words:
        for word in transcript.words:
            word_timestamps.append({
                "text": word.text,
                "start": word.start,
                "end": word.end
            })
    return word_timestamps

if __name__ == "__main__":
    # Example usage:
    # Set your AssemblyAI API key as an environment variable:
    # export ASSEMBLYAI_API_KEY="YOUR_API_KEY"

    # For testing, you can use a sample audio file.
    # Replace with your actual audio file path.
    sample_audio_file = "path/to/your/audio.wav" 

    try:
        timestamps = get_timestamped_transcript(sample_audio_file)
        for word_data in timestamps:
            print(f"Word: {word_data['text']}, Start: {word_data['start']}ms, End: {word_data['end']}ms")
    except Exception as e:
        print(f"An error occurred: {e}")
