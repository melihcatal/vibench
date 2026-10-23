import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_with_timestamps(audio_file_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

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
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        for word_info in result.alternatives[0].words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, Start time: {}, End time: {}'.format(
                word, start_time, end_time))

if __name__ == '__main__':
    transcribe_with_timestamps('path/to/your/audiofile.wav')