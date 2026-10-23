from typing import Dict, Any
from deepgram.types.live import LiveOptions

def get_live_options(
    model: str = "nova-2",
    language: str = "en-US",
    punctuate: bool = True,
    interim_results: bool = True,
    smart_format: bool = True,
    encoding: str = "linear16",
    sample_rate: int = 16000,
    channels: int = 1,
) -> LiveOptions:
    return LiveOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
        smart_format=smart_format,
        encoding=encoding,
        sample_rate=sample_rate,
        channels=channels,
    )
