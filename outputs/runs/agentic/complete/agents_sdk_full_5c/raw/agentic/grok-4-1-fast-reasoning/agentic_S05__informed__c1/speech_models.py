from typing import Any
from deepgram import LiveOptions

DEFAULT_MODEL = 'nova-2-general'

def get_stt_live_options(
    *,
    model: str = DEFAULT_MODEL,
    language: str = 'en',
    punctuate: bool = True,
    interim_results: bool = True,
    **extra: Any
) -> LiveOptions:
    kwargs = {
        'model': model,
        'language': language,
        'punctuate': punctuate,
        'interim_results': interim_results,
        **extra
    }
    return LiveOptions(**kwargs)
