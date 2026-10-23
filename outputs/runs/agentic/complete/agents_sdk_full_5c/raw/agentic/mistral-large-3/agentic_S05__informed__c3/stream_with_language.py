from speech_client import get_deepgram_client
from partial_results import handle_partial_result

def start_stream_with_language(language="en-US", punctuate=True):
    client = get_deepgram_client()
    options = {
        "language": language,
        "punctuate": punctuate,
        "model": "nova-2",  # Deepgram's concrete model identifier
    }
    deepgram_socket = client.listen.live.v("latest", options)

    def on_message(ws, message):
        handle_partial_result(message)

    deepgram_socket.registerHandler(deepgram_socket.event.CLOSE, lambda _: print("Deepgram connection closed"))
    deepgram_socket.registerHandler(deepgram_socket.event.MESSAGE, on_message)

    return deepgram_socket