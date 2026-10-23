import os
from ibm_watson import SpeechToTextV1

class SpeechClient:
    def __init__(self):
        api_key = os.getenv('IBM_STT_APIKEY')
        url = os.getenv('IBM_STT_URL')
        self.client = SpeechToTextV1(api_key=api_key, url=url)

    def recognize_audio(self, audio_bytes, content_type='audio/l16; rate=16000'):
        """Synchronous recognition (non-streaming) for simple calls."""
        return self.client.recognize(audio=audio_bytes, content_type=content_type).get_result()

    def start_stt_async(self, audio_source, callback, language_model='en-US_BroadbandModel'):
        """Asynchronous WebSocket streaming. Callback receives JSON events."""
        self.client.start_stt_async(
            callback=callback,
            audio=audio_source,
            content_type='audio/l16; rate=16000',
            language_model=language_model,
        )

    def stop_stt_async(self):
        self.client.stop_stt_async()

if __name__ == '__main__':
    # Simple test: load a test audio file and perform synchronous recognition
    from ibm_watson import ApiException
    client = SpeechClient()
    try:
        with open('sample.wav', 'rb') as f:
            resp = client.recognize(audio=f).get_result()
        print('Synchronous transcription:', resp['results'][0]['alternatives'][0]['transcript'])
    except ApiException as e:
        print('Recognition error:', e)
