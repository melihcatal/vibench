from google.cloud import texttospeech

def create_client():
    text_to_speech_client = texttospeech.TextToSpeechClient()
    return text_to_speech_client

if __name__ == '__main__':
    client = create_client()