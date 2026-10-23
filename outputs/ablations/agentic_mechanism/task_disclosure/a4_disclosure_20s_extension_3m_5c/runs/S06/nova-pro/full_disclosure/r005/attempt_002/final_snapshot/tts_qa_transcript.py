from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_file_path):
    """Transcribes an audio file to text using Google Cloud Speech-to-Text API"""
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        audio = speech.RecognitionAudio(content=audio_file.read())

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    audio_file_path = 'path/to/audio/file'
    transcribe_audio(audio_file_path)