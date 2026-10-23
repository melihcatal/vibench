from google.cloud import speech_v1p1beta1 as speech

def get_speech_client(project_id: str, location: str = 'global'):
    config = {"encoding": "LINEAR16",
              "sample_rate_hertz": 16000,
              "language_code": 'en-US'}
    client = speech.SpeechClient()
    return client

if __name__ == '__main__':
    project_id = 'YOUR_PROJECT_ID'
    client = get_speech_client(project_id)
    print(f'Client created for project: {project_id}')
