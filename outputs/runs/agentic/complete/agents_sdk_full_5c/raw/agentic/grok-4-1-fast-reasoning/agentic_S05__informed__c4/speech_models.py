from dataclasses import dataclass
from typing import Optional
from deepgram import LiveOptions

@dataclass
class StreamingConfig:
    model: str = "nova-2"
    version: str = "1"
    language: Optional[str] = "en"
    punctuate: bool = True
    smart_format: bool = True
    interim_results: bool = True

def create_live_options(config: StreamingConfig) -> LiveOptions:
    options_dict = {
        "model": config.model,
        "punctuate": config.punctuate,
        "smart_format": config.smart_format,
        "interim_results": config.interim_results,
    }
    if config.language:
        options_dict["language"] = config.language
    return LiveOptions(**options_dict)
