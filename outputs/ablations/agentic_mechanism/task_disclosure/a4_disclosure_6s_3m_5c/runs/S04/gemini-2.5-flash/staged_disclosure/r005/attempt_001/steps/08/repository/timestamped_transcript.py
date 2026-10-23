from google.cloud import speech

def transcribe_audio_with_timestamps(audio_file_path):
    """Transcribes the given audio file and returns word-level timestamps."""

    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Or other appropriate encoding
        sample_rate_hertz=16000, # Or other appropriate sample rate
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)

    word_timestamps = []
    for result in response.results:
        for word_info in result.alternatives[0].words:
            word_timestamps.append(
                {
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                }
            )
    return word_timestamps

if __name__ == "__main__":
    # Example usage (replace with your audio file)
    # Ensure you have Google Cloud authentication set up (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # For testing, you might need a .wav file with LINEAR16 encoding and 16000 sample rate.
    # audio_path = "path/to/your/audio.wav"
    # timestamps = transcribe_audio_with_timestamps(audio_path)
    # for ts in timestamps:
    #     print(f"Word: {ts["word"]}, Start: {ts["start_time"]:.2f}s, End: {ts["end_time"]:.2f}s")
    print("To use, call transcribe_audio_with_timestamps(audio_file_path) with your audio file.")
    print("Ensure Google Cloud authentication is set up and the correct audio encoding/sample rate are configured.")
