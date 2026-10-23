import os
import queue
import threading
from deepgram import DeepgramClient, LiveTranscriptionEvents

def stream_chunks(audio_chunks):
    &quot;&quot;&quot;Streams audio chunks from an iterable source and yields interim transcripts.&quot;&quot;&quot;
    api_key = os.getenv(&quot;DEEPGRAM_API_KEY&quot;)
    client = DeepgramClient(api_key)

    transcript_queue = queue.Queue()

    def on_transcript(result):
        if result.channel and result.channel.alternatives:
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                transcript_queue.put(transcript)

    def on_close(_):
        transcript_queue.put(None)

    connection = client.listen.live.v(&quot;1&quot;)
    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.on(LiveTranscriptionEvents.Close, on_close)

    options = {
        &quot;model&quot;: &quot;nova-2&quot;,
        &quot;language&quot;: &quot;en-US&quot;,
        &quot;punctuate&quot;: True,
        &quot;interim_results&quot;: True,
        &quot;smart_format&quot;: True,
    }
    connection.start(options)

    def send_loop():
        try:
            for chunk in audio_chunks:
                connection.send(chunk)
        finally:
            connection.finish()

    sender_thread = threading.Thread(target=send_loop, daemon=True)
    sender_thread.start()

    while True:
        transcript = transcript_queue.get()
        if transcript is None:
            break
        yield transcript