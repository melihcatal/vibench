from google.cloud import speech_v1p1beta1 as speech
import pyaudio
import queue
import threading


class LanguageAwareStreamingRecognizer:
    def __init__(
        self, language_code="en-US", enable_punctuation=True, sample_rate=16000
    ):
        self.client = speech.SpeechClient()
        self.language_code = language_code
        self.enable_punctuation = enable_punctuation
        self.sample_rate = sample_rate
        self.audio_interface = pyaudio.PyAudio()

    def create_recognition_config(self):
        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.sample_rate,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_punctuation,
            enable_word_time_offsets=True,
            enable_word_confidence=True,
            model="latest_long",
            use_enhanced=True,
        )

    def create_streaming_config(self):
        config = self.create_recognition_config()

        return speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
            speech_contexts=[
                speech.SpeechContext(
                    phrases=["meeting", "agenda", "action items", "next steps"],
                    boost=10.0,
                )
            ],
        )

    class AudioStream:
        def __init__(self, rate, chunk):
            self.rate = rate
            self.chunk = chunk
            self._buff = queue.Queue()
            self.closed = True

        def __enter__(self):
            self._audio_interface = pyaudio.PyAudio()
            self._audio_stream = self._audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=self._fill_buffer,
            )
            self.closed = False
            return self

        def __exit__(self, type, value, traceback):
            self._audio_stream.stop_stream()
            self._audio_stream.close()
            self.closed = True
            self._buff.put(None)
            self._audio_interface.terminate()

        def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
            self._buff.put(in_data)
            return None, pyaudio.paContinue

        def generator(self):
            while not self.closed:
                chunk = self._buff.get()
                if chunk is None:
                    return
                data = [chunk]

                while True:
                    try:
                        chunk = self._buff.get(block=False)
                        if chunk is None:
                            return
                        data.append(chunk)
                    except queue.Empty:
                        break

                yield b"".join(data)

    def start_streaming_recognizer(self):
        streaming_config = self.create_streaming_config()

        with self.AudioStream(rate=self.sample_rate, chunk=1024) as stream:
            audio_generator = stream.generator()

            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = self.client.streaming_recognize(streaming_config, requests)

            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                is_final = result.is_final

                yield {
                    "transcript": transcript,
                    "is_final": is_final,
                    "language": self.language_code,
                    "punctuation_enabled": self.enable_punctuation,
                    "confidence": result.alternatives[0].confidence
                    if is_final
                    else None,
                    "stability": result.stability
                    if hasattr(result, "stability")
                    else None,
                }


def stream_with_language_settings(language_code="en-US", punctuation=True):
    recognizer = LanguageAwareStreamingRecognizer(
        language_code=language_code, enable_punctuation=punctuation
    )

    return recognizer.start_streaming_recognizer()


if __name__ == "__main__":
    print("Starting English streaming with punctuation...")
    for result in stream_with_language_settings("en-US", True):
        prefix = "FINAL" if result["is_final"] else "PARTIAL"
        print(f"[{prefix}] [{result['language']}] {result['transcript']}")
