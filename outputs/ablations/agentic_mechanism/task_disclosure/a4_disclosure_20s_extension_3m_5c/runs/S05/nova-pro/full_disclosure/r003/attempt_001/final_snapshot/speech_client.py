from google.cloud import speech_v1p1beta1 as speech

def create_speech_client():
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )
    client = speech.SpeechClient()
    return client, config

if __name__ == '__main__':
    client, config = create_speech_client()
    print('Speech client created successfully.')