import asyncio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import microphone

class StreamingRecognize(RecognizeCallback):
    def __init__(self):
        super().__init__()
        self.partial_transcripts = []

    def on_connected(self):
        print('Connected to Watson Speech to Text')

    def on_data(self, data):
        # data contains interim and final results
        results = data.get('results', [])
        for result in results:
            alternatives = result.get('alternatives', [])
            if not alternatives:
                continue
            transcript = alternatives[0].get('transcript', '')
            timestamp = data.get('timestamp')
            if result.get('final', False):
                print('Final transcript:', transcript)
            else:
                print('Interim transcript:', transcript)
            self.partial_transcripts.append((transcript, result.get('final', False)))

    def on_error(self, error):
        print('Error received: {}'.format(error))

async def stream_microphone():
    # Configure credentials
    api_key = "${IBM_STT_APIKEY}"
    url = "${IBM_STT_URL}"
    service = SpeechToTextV1(api_key=api_key, url=url)

    audio_source = AudioSource(microphone.AudioStream())
    streaming_callback = StreamingRecognize()

    service.start_stt_async(audio_source, streaming_callback, recognize_rate=10)
    await asyncio.Event().wait()  # keep running

if __name__ == "__main__":
    asyncio.run(stream_microphone())