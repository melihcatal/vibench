import asyncio
import os
import azure.cognitiveservices.speech as speechsdk

# Azure AI Speech streaming configuration
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

async def stream_audio_chunks(audio_chunk_generator):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language = "en-US"

    class CustomAudioInputStream(speechsdk.audio.PullAudioInputStreamCallback):
        def __init__(self, audio_chunks):
            super().__init__()
            self._audio_chunks = audio_chunks
            self._buffer = b""
            self._chunk_iterator = iter(audio_chunks)

        def read(self, size: int) -> bytes:
            while len(self._buffer) < size:
                try:
                    chunk = next(self._chunk_iterator)
                    self._buffer += chunk
                except StopIteration:
                    break
            
            data_to_return = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return data_to_return

        def close(self):
            pass

    audio_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
    
    async def recognize_stream():
        audio_input_stream = CustomAudioInputStream(audio_chunk_generator)
        audio_config = speechsdk.audio.AudioConfig(stream=audio_input_stream, format=audio_format)
        
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False
        def stop_cb(evt):
            nonlocal done
            done = True

        speech_recognizer.recognized.connect(lambda evt: print(f"RECOGNIZED: {evt.result.text}"))
        speech_recognizer.canceled.connect(lambda evt: print(f"CANCELED: {evt.cancellation_details.reason}"))
        speech_recognizer.session_stopped.connect(stop_cb)
        
        speech_recognizer.start_continuous_recognition()
        while not done:
            await asyncio.sleep(0.5)
        speech_recognizer.stop_continuous_recognition()

    await recognize_stream()
