from google.cloud import speech_v1p1beta1 as speech

def transcribe_with_timestamps(audio_file_path):
    """Transcribes the given audio file and returns word timestamps."""
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        for alternative in result.alternatives:
            print('Transcript: {}'.format(alternative.transcript))
            for word_info in alternative.words:
                print('Word: {}, Start Time: {}, End Time: {}'.format(
                    word_info.word, word_info.start_time, word_info.end_time))

# Example usage:
# transcribe_with_timestamps('path_to_audio_file.wav')