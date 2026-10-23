import azure.cognitiveservices.speech as speechsdk
import asyncio
from speech_client import get_speech_config, get_audio_config_from_stream
from speech_models import AudioChunk

async def stream_audio_chunks(audio_chunks_async_iterator):
    speech_config = get_speech_config()
    audio_config = get_audio_config_from_stream()
    audio_input_stream = speechsdk.audio.PushAudioInputStream(audio_config.stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Starting chunk streaming...")

    done = False
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED: {} ({})'.format(evt.reason, evt.error_details)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition_async()

    try:
        async for chunk in audio_chunks_async_iterator:
            if isinstance(chunk, AudioChunk):
                audio_input_stream.write(chunk.data)
            else:
                print("Received non-AudioChunk object in stream.")
    except Exception as e:
        print(f"Error processing audio chunks: {e}")
    finally:
        audio_input_stream.close()

    while not done:
        await asyncio.sleep(0.5)

    speech_recognizer.stop_continuous_recognition_async()

if __name__ == "__main__":
    # Example async iterator for demonstration
    async def generate_chunks():
        for i in range(5):
            # Simulate receiving audio data
            await asyncio.sleep(1)
            yield AudioChunk(data=b"Simulated audio data chunk {i}")

    asyncio.run(stream_audio_chunks(generate_chunks()))
