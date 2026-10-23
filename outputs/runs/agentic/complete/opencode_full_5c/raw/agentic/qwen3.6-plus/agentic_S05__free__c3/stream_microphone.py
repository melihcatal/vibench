import os
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIClientError


def get_speech_client():
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        return speech.SpeechClient.from_service_account_file(credentials_path)
    return speech.SpeechClient()


def stream_microphone_audio(
    sample_rate=16000,
    chunk_size=4096,
    language_code="en-US",
    model="latest_long",
    enable_automatic_punctuation=True,
    interim_results=True,
    max_alternatives=1,
):
    client = get_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=language_code,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
        max_alternatives=max_alternatives,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )

    audio_format = pyaudio.paInt16
    channels = 1

    def audio_generator():
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=audio_format,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size,
        )
        try:
            while True:
                data = stream.read(chunk_size, exception_on_overflow=False)
                yield speech.StreamingRecognizeRequest(audio_content=data)
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()

    requests = audio_generator()
    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests,
    )

    for response in responses:
        for result in response.results:
            transcript = (
                result.alternatives[0].transcript if result.alternatives else ""
            )
            is_final = result.is_final
            confidence = (
                result.alternatives[0].confidence if result.alternatives else 0.0
            )
            yield {
                "transcript": transcript,
                "is_final": is_final,
                "confidence": confidence,
                "stability": result.stability,
                "result_end_time": result.result_end_time.total_seconds()
                if result.result_end_time
                else 0.0,
            }
