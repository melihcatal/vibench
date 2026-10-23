import speech_client

def stream_chunks(audio_chunks):
    client = speech_client.get_client()
    with client.start_stream() as stream:
        for chunk in audio_chunks:
            stream.send_audio(chunk)
            yield stream.receive_transcript()