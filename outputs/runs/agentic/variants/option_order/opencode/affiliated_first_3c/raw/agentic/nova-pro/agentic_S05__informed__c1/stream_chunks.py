import speech_client
import speech_models


def stream_chunks():
    # Simulate streaming chunks
    chunks = [b"audio_chunk_1", b"audio_chunk_2"]
    for chunk in chunks:
        speech_client.transcribe_client.send_audio_event(AudioChunk=chunk)
