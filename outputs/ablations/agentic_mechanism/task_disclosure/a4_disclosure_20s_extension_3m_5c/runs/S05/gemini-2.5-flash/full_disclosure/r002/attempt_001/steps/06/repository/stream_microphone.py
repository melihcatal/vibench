import asyncio
import queue
import sounddevice as sd

from google.cloud import speech

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms chunks

class MicrophoneStream:
    """Opens a recording stream as an Iterable object to be fed to the Speech API."""

    def __init__(self, rate=SAMPLE_RATE, chunk_size=CHUNK_SIZE):
        self._rate = rate
        self._chunk_size = chunk_size
        self._buff = asyncio.Queue()
        self.closed = True

    async def __aenter__(self):
        self.closed = False
        self._audio_stream = sd.RawInputStream(
            samplerate=self._rate,
            blocksize=self._chunk_size,
            dtype="int16",
            channels=1,
            callback=self._fill_buffer,
        )
        self._audio_stream.start()
        return self

    async def __aexit__(self, type, value, traceback):
        self._audio_stream.stop()
        self._audio_stream.close()
        self.closed = True
        # Signal the end of the audio input
        await self._buff.put(None)

    def _fill_buffer(self, in_data, frame_count, time_info, status):
        """Continuously collect audio data from the stream into the buffer."""
        if status:
            print(status)
        self._buff.put_nowait(in_data)

    async def __aiter__(self):
        while not self.closed:
            chunk = await self._buff.get()
            if chunk is None:
                return
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

async def stream_microphone_audio():
    """Streams audio from the microphone to the Google Cloud Speech-to-Text API and yields interim transcripts."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async with MicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as stream:
        requests = stream.__aiter__()
        responses = await client.streaming_recognize(request_iterator=requests, config=streaming_config)

        async for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                yield f"Final: {transcript}"
            else:
                yield f"Interim: {transcript}"

