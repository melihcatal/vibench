from google.cloud import speech_v1p1beta1 as speech

def stream_with_language():
    config = {"encoding": "LINEAR16",
             "sample_rate_hertz": 16000,
             "language_code": "en-US",
             "enable_automatic_punctuation": True}
    client = speech.SpeechClient()
    with open('audio.raw', 'rb') as audio_file:
        audio = client.streaming_recognize(config=config,
                                          audio=audio_file)
        for response in audio:
            for result in response.results:
                print(result.alternatives[0].transcript)

if __name__ == '__main__':
    stream_with_language()