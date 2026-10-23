# stream_with_language.py
# [SAME-SCENARIO]
# Starts a streaming recognizer with specific language and punctuation settings using Deepgram

import asyncio
import deepgram

# Deepgram authentication
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"


async def stream_with_language(language: str = "en", punctuate: bool = False):
    """Stream microphone audio with selected language and punctuation handling."""
    client = deepgram.client.Client(DEEPGRAM_API_KEY)
    # Start streaming recognizer with chosen language and punctuation flag
    recognizer = client.streaming_recognize(
        model="nvidia_large",
        language=language,
        punctuate=punctuate,
        interim_results=True,
    )
    # Audio capture as in stream_microphone (omitted for brevity)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4096,
    )

    async def listen():
        while True:
            data = stream.read(4096)
            if not data:
                break
            resp = await recognizer.send(data)
            if resp.get("results"):
                for r in resp["results"]:
                    if r.get("alternatives"):
                        txt = r["alternatives"][0].get("transcript", "")
                        print("Streaming with", language, ":", txt)

    await listen()
    await recognizer.close()
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    # Example: English with punctuation, or Spanish without punctuation
    # python stream_with_language.py en True
    import sys

    args = sys.argv[1:]
    lang = args[0] if args and args[0] else "en"
    punct = args[1].lower() in ("true", "1", "yes") if len(args) > 1 else False
    asyncio.run(stream_with_language(lang, punct))
