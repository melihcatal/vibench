import asyncio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client

# ---------------------------------------------------------------------------
# SAME-SCENARIO: stream_with_language.py                                  #
# Starts a streaming recognizer with a specific language, diarization,
# and automatic punctuation options.
# ---------------------------------------------------------------------------

async def run(language_code: str = "es-ES"):
    client = get_speech_client()
    # Choose a model that supports language detection and punctuation
    model = "default"  # e.g., "default", "phone_call", "video"
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model=model,
        # Optional: speaker diarization (example settings)
        # diarization_config=speech.SpeakerDiarizationConfig(
        #     enable_speaker_diarization=True,
        #     min_speaker_count=2,
        #     max_speaker_count=4,
        # ),
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        # Enable single‑utterance for short phrases (uncomment if desired)
        # single_utterance=True,
    )
    # Create a dummy generator that yields silent audio to keep the stream alive
    async def silent_source():
        while True:
            yield b"\0" * 1600  # 100 ms of silence
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in silent_source())
    responses = client.streaming_recognize(streaming_config, requests)
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                print(f"{transcript}{' (final)' if is_final else ''}")

if __name__ == "__main__":
    # Launch with Spanish language example; change the argument as needed
    asyncio.run(run())
