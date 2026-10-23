import os
import queue
import threading
import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents

def stream_microphone():
    &quot;&quot;&quot;Streams microphone audio and yields interim transcripts.&quot;&quot;&quot;
    api_key = os.getenv(&quot;DEEPGRAM_API_KEY&quot;)
    client = DeepgramClient(api_key)

    transcript_queue = queue.Queue()

    def on_transcript(result):
        if result.channel and result.channel.alternatives:
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                transcript_queue.put(transcript)

    def on_error(result):
        print(f&quot;Error: {result}&quot;)

    connection = client.listen.live.v(&quot;1&quot;)
    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.on(LiveTranscriptionEvents.Close, lambda: transcript_queue.put(None))
    connection.on(LiveTranscriptionEvents.Error, on_error)

    options = {
        &quot;model&quot;: &quot;nova-2&quot;,
        &quot;language&quot;: &quot;en-US&quot;,
        &quot;punctuate&quot;: True,
        &quot;interim_results&quot;: True,
        &quot;smart_format&quot;: True,
    }
    connection.start(options)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    def audio_loop():
        try:
            while True:
                try:
                    data = stream.read(1024, exception_on_overflow=False)
                except OSError:
                    continue
                connection.send(data)
        except Exception:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            connection.finish()

    audio_thread = threading.Thread(target=audio_loop, daemon=True)
    audio_thread.start()

    while True:
        transcript = transcript_queue.get()
        if transcript is None:
            break
        yield transcript