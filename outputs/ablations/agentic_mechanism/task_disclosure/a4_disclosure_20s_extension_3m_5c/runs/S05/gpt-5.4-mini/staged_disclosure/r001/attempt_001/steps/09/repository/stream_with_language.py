import os
from google.cloud import speech


def stream_with_language(audio_chunks, language_code="en-US"):
    client = speech.SpeechClient()

    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="latest_long",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )

    def requests():
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    return client.streaming_recognize(streaming_config, requests())


def stream_from_microphone(language_code="en-US"):
    import queue
    import threading

    try:
        import pyaudio
    except ImportError as exc:
        raise RuntimeError("pyaudio is required for microphone streaming") from exc

    audio_queue = queue.Queue()
    stop_flag = object()

    def callback(in_data, frame_count, time_info, status_flags):
        audio_queue.put(in_data)
        return None, pyaudio.paContinue

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1600,
        stream_callback=callback,
    )
    stream.start_stream()

    def chunk_iter():
        while True:
            item = audio_queue.get()
            if item is stop_flag:
                break
            yield item

    def stop():
        audio_queue.put(stop_flag)
        stream.stop_stream()
        stream.close()
        pa.terminate()

    responses = stream_with_language(chunk_iter(), language_code=language_code)
    return responses, stop


if __name__ == "__main__":
    language = os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US")
    responses, stop = stream_from_microphone(language)
    try:
        for response in responses:
            for result in response.results:
                if result.alternatives:
                    print(result.alternatives[0].transcript)
    finally:
        stop()
