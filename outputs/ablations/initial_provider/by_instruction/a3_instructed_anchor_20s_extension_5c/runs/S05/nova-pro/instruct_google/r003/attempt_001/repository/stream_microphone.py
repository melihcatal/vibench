import pyaudio
import speech_client

def stream_microphone():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)
    client = speech_client.get_speech_client()
    config = speech_client.create_streaming_config()
    streaming_requests = []
    while True:
        data = stream.read(1024)
        streaming_requests.append(speech.types.StreamingRecognizeRequest(audio_content=data))
        if len(streaming_requests) == 1:
            streaming_requests.insert(0, speech.types.StreamingRecognizeRequest(streaming_config=config))
        responses = client.streaming_recognize(streaming_requests)
        for response in responses:
            for result in response.results:
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                yield transcript, is_final
        streaming_requests = []