import os
from deepgram import DeepgramClient, LiveOptions, DeepgramClientOptions

def get_speech_client():
    """Initializes the Deepgram client from environment variables."""
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")

    config = DeepgramClientOptions(
        verbose=0,  # Suppress verbose logging
    )
    
    deepgram_client = DeepgramClient(api_key, config)
    return deepgram_client

def get_live_options(
    model="nova-2",
    language="en-US",
    punctuate=False,
    smart_format=True,
    interim_results=True,
    **kwargs
):
    """Creates a LiveOptions object with common settings."""
    options = LiveOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        smart_format=smart_format,
        interim_results=interim_results,
        **kwargs
    )
    return options
