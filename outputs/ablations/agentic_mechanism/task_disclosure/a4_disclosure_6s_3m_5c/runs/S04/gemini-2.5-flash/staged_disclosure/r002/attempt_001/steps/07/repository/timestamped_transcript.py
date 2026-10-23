from google.cloud import speech

def get_timestamped_transcript(audio_file_path: str):
    """
    Transcribes an audio file and returns word-level timestamps.

    Args:
        audio_file_path: The path to the audio file to transcribe.

    Returns:
        A list of dictionaries, where each dictionary represents a word
        and contains the word, its start time, and its end time.
    """
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

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
