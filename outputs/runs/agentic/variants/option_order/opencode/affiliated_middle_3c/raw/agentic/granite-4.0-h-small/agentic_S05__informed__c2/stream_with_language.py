import deepgram

DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"


async def stream_with_language(language="en-US", punctuation=True):
    """Starts a streaming recognizer with language and punctuation settings using Deepgram.
    Args:
        language (str): BCP-47 language tag (default "en-US").
        punctuation (bool): Enable punctuation in transcript (default True).
    """
    client = deepgram.StreamingClient(DEEPGRAM_API_KEY)
    async with client.start_language(language, punctuate=punctuation) as stream:
        async for result in stream.listen():
            if result.get("is_final"):
                print("FINAL:", result["alternatives"][0]["transcript"])
            else:
                print("INTERIM:", result["alternatives"][0]["transcript"])


# Example (not executed here)
# asyncio.run(stream_with_language(language="es-ES", punctuation=False))
