import os
from deepgram import DeepgramClient

def get_deepgram_client() -> DeepgramClient:
    """
    Provides a configured DeepgramClient instance.
    Requires DEEPGRAM_API_KEY environment variable to be set.
    """
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set")
    return DeepgramClient(api_key)


def get_deepgram_live_options(language: str = "en-US", punctuate: bool = True, interim_results: bool = True):
    """
    Provides common Deepgram LiveOptions for streaming.
    """
    from deepgram import LiveOptions
    return LiveOptions(
        punctuate=punctuate,
        language=language,
        interim_results=interim_results,
    )

if __name__ == "__main__":
    # Example usage:
    # try:
    #     client = get_deepgram_client()
    #     print("Deepgram client initialized successfully.")
    # except ValueError as e:
    #     print(e)
    # options = get_deepgram_live_options(language="es", punctuate=False)
    # print(f"Deepgram Live Options: {options}")
    pass
