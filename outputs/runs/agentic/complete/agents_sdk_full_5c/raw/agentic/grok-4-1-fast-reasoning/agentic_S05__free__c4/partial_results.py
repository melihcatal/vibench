import queue
from deepgram import LiveTranscriptionEvents
from typing import Generator, Dict, Any

def handle_partial_and_final(connection) -> Generator[Dict[str, Any], None, None]:
    &quot;&quot;&quot;Handles partial and final streaming recognition events, yielding dicts with text and final flag.&quot;&quot;&quot;
    result_queue = queue.Queue()

    def on_transcript(result):
        text = &quot;&quot;
        is_final = False
        if result.channel and result.channel.alternatives:
            text = result.channel.alternatives[0].transcript
            is_final = result.speech_final
        result_queue.put({&quot;text&quot;: text, &quot;is_final&quot;: is_final})

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    while True:
        yield result_queue.get()