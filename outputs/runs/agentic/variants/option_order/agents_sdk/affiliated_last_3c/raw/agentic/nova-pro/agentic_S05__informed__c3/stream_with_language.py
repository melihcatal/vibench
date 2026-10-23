import speech_client

def stream_with_language(language, punctuation):
    client = speech_client.get_client()
    with client.start_stream(language=language, punctuation=punctuation) as stream:
        while True:
            audio_data = client.get_microphone_data()
            if not audio_data:
                break
            stream.send_audio(audio_data)
            yield stream.receive_transcript()