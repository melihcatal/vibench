from typing import Optional
from deepgram.utils.live import LiveOptions

def get_live_options(
    model: str = "nova-2-general",
    language: str = "en-US",
    punctuate: bool = True,
    interim_results: bool = True,
    smart_format: bool = True,
) -> LiveOptions:
    return LiveOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
        smart_format=smart_format,
    )
